package backend.backend.service;

import backend.backend.dto.AlternativeBlock;
import backend.backend.dto.BlockPlanRequest;
import backend.backend.dto.BlockPlanResponse;
import backend.backend.dto.RecommendedBlock;
import backend.backend.model.Corridor;
import backend.backend.model.MaintenancePlan;
import backend.backend.model.MaintenanceTask;
import backend.backend.repository.MaintenancePlanRepository;
import backend.backend.repository.MaintenanceTaskRepository;
import org.springframework.stereotype.Service;

import java.time.LocalDate;
import java.time.LocalTime;
import java.time.temporal.ChronoUnit;
import java.util.ArrayList;
import java.util.Comparator;
import java.util.List;

@Service
public class PlanService {

    private final MaintenanceTaskRepository taskRepository;
    private final MaintenancePlanRepository planRepository;
    private final CorridorService corridorService;
    private final ConflictDetectionService conflictDetectionService;
    private final GoodsTrainForecastService goodsTrainForecastService;
    private final OptimizationService optimizationService;

    public PlanService(
            MaintenanceTaskRepository taskRepository,
            MaintenancePlanRepository planRepository,
            CorridorService corridorService,
            ConflictDetectionService conflictDetectionService,
            GoodsTrainForecastService goodsTrainForecastService,
            OptimizationService optimizationService) {

        this.taskRepository = taskRepository;
        this.planRepository = planRepository;
        this.corridorService = corridorService;
        this.conflictDetectionService = conflictDetectionService;
        this.goodsTrainForecastService = goodsTrainForecastService;
        this.optimizationService = optimizationService;
    }

    public BlockPlanResponse generatePlan(
            BlockPlanRequest request) {

        if (request == null) {
            throw new IllegalArgumentException(
                    "Block plan request is required."
            );
        }

        Corridor corridor =
                corridorService.getByCorridorId(
                        request.corridorId()
                );

        validateCorridor(corridor);

        MaintenanceTask task =
                findPrimaryTask(request);

        int duration =
                resolveDuration(
                        request,
                        task
                );

        MaintenancePlan existingPlan =
                findExistingPlan(
                        task.getTaskId(),
                        request.corridorId(),
                        request.date()
                );

        if (existingPlan != null
                && isExistingPlanStillValid(existingPlan)) {

            RecommendedBlock block =
                    new RecommendedBlock(
                            existingPlan.getCorridorId(),
                            existingPlan.getDate(),
                            existingPlan.getStartTime().toString(),
                            existingPlan.getEndTime().toString(),
                            existingPlan.getDuration(),
                            existingPlan.getTrainImpact(),
                            calculateExistingPlanScore(
                                    task,
                                    corridor,
                                    existingPlan
                            ),
                            "Existing valid maintenance plan returned. "
                                    + "Duplicate planning was prevented."
                    );

            return new BlockPlanResponse(
                    true,
                    block,
                    List.of()
            );
        }

        List<CandidateBlock> candidates =
                findCandidates(
                        request,
                        corridor,
                        task,
                        duration,
                        existingPlan
                );

        if (candidates.isEmpty()) {
            throw new IllegalArgumentException(
                    "No safe maintenance block is available for corridor "
                            + request.corridorId()
                            + " on "
                            + request.date()
            );
        }

        candidates.sort(
                Comparator
                        .comparingDouble(
                                CandidateBlock::score
                        )
                        .reversed()
                        .thenComparing(
                                CandidateBlock::startTime
                        )
        );

        CandidateBlock best =
                candidates.get(0);

        MaintenancePlan savedPlan =
                saveOrUpdatePlan(
                        existingPlan,
                        task,
                        request,
                        duration,
                        best
                );

        RecommendedBlock recommended =
                new RecommendedBlock(
                        savedPlan.getCorridorId(),
                        savedPlan.getDate(),
                        savedPlan.getStartTime().toString(),
                        savedPlan.getEndTime().toString(),
                        savedPlan.getDuration(),
                        savedPlan.getTrainImpact(),
                        best.score(),
                        buildReason(
                                task,
                                corridor,
                                best
                        )
                );

        List<AlternativeBlock> alternatives =
                candidates.stream()
                        .skip(1)
                        .limit(3)
                        .map(candidate ->
                                new AlternativeBlock(
                                        request.corridorId(),
                                        request.date(),
                                        candidate.startTime()
                                                .toString(),
                                        candidate.endTime()
                                                .toString(),
                                        duration,
                                        candidate.trainImpact(),
                                        candidate.score(),
                                        buildReason(
                                                task,
                                                corridor,
                                                candidate
                                        )
                                )
                        )
                        .toList();

        return new BlockPlanResponse(
                true,
                recommended,
                alternatives
        );
    }

    private MaintenanceTask findPrimaryTask(
            BlockPlanRequest request) {

        if (request.taskId() == null
                || request.taskId().isBlank()) {

            throw new IllegalArgumentException(
                    "Task ID is required."
            );
        }

        MaintenanceTask task =
                taskRepository
                        .findByTaskId(request.taskId())
                        .orElseThrow(() ->
                                new IllegalArgumentException(
                                        "Maintenance task not found: "
                                                + request.taskId()
                                )
                        );

        if (!isPending(task)) {
            throw new IllegalArgumentException(
                    "Maintenance task is not pending: "
                            + request.taskId()
            );
        }

        if (request.department() != null
                && task.getDepartment() != null
                && !task.getDepartment()
                .equalsIgnoreCase(
                        request.department()
                )) {

            throw new IllegalArgumentException(
                    "Task "
                            + request.taskId()
                            + " does not belong to department "
                            + request.department()
            );
        }

        if (task.getLocation() == null
                || !task.getLocation()
                .equalsIgnoreCase(
                        request.corridorId()
                )) {

            throw new IllegalArgumentException(
                    "Task "
                            + request.taskId()
                            + " is not assigned to corridor "
                            + request.corridorId()
            );
        }

        return task;
    }

    private MaintenancePlan findExistingPlan(
            String taskId,
            String corridorId,
            LocalDate date) {

        return planRepository
                .findByTaskId(taskId)
                .stream()
                .filter(plan ->
                        plan.getCorridorId() != null
                                &&
                                corridorId.equalsIgnoreCase(
                                        plan.getCorridorId()
                                ))
                .filter(plan ->
                        date.equals(plan.getDate()))
                .filter(plan ->
                        !isHistorical(
                                plan.getStatus()
                        ))
                .findFirst()
                .orElse(null);
    }

    private boolean isExistingPlanStillValid(
            MaintenancePlan plan) {

        if (plan == null
                || plan.getCorridorId() == null
                || plan.getDate() == null
                || plan.getStartTime() == null
                || plan.getEndTime() == null) {

            return false;
        }

        if (isHistorical(plan.getStatus())) {
            return true;
        }

        boolean maintenanceConflict =
                conflictDetectionService
                        .hasMaintenanceConflict(
                                plan.getCorridorId(),
                                plan.getDate(),
                                plan.getStartTime(),
                                plan.getEndTime(),
                                plan.getId()
                        );

        if (maintenanceConflict) {
            return false;
        }

        boolean blockRequestConflict =
                conflictDetectionService
                        .hasBlockRequestConflict(
                                plan.getCorridorId(),
                                plan.getDate(),
                                plan.getStartTime(),
                                plan.getEndTime()
                        );

        if (blockRequestConflict) {
            return false;
        }

        int highPriorityTrainConflicts =
                conflictDetectionService
                        .countHighPriorityTrainConflicts(
                                plan.getCorridorId(),
                                plan.getStartTime(),
                                plan.getEndTime()
                        );

        return highPriorityTrainConflicts == 0;
    }

    private List<CandidateBlock> findCandidates(
            BlockPlanRequest request,
            Corridor corridor,
            MaintenanceTask task,
            int duration,
            MaintenancePlan existingPlan) {

        List<CandidateBlock> candidates =
                new ArrayList<>();

        LocalTime currentStart =
                corridor.getAvailableStart();

        LocalTime availableEnd =
                corridor.getAvailableEnd();

        while (!currentStart
                .plusMinutes(duration)
                .isAfter(availableEnd)) {

            LocalTime currentEnd =
                    currentStart.plusMinutes(duration);

            boolean maintenanceConflict =
                    conflictDetectionService
                            .hasMaintenanceConflict(
                                    request.corridorId(),
                                    request.date(),
                                    currentStart,
                                    currentEnd,
                                    existingPlan == null
                                            ? null
                                            : existingPlan.getId()
                            );

            boolean blockRequestConflict =
                    conflictDetectionService
                            .hasBlockRequestConflict(
                                    request.corridorId(),
                                    request.date(),
                                    currentStart,
                                    currentEnd
                            );

            int trainConflicts =
                    conflictDetectionService
                            .countTrainConflicts(
                                    request.corridorId(),
                                    currentStart,
                                    currentEnd
                            );

            int highPriorityTrainConflicts =
                    conflictDetectionService
                            .countHighPriorityTrainConflicts(
                                    request.corridorId(),
                                    currentStart,
                                    currentEnd
                            );

            int goodsTrainCount =
                    goodsTrainForecastService
                            .getOverlappingGoodsTrainCount(
                                    request.corridorId(),
                                    request.date(),
                                    currentStart,
                                    currentEnd
                            );

            if (!maintenanceConflict
                    && !blockRequestConflict
                    && highPriorityTrainConflicts == 0) {

                double score =
                        optimizationService.calculateScore(
                                task,
                                corridor,
                                trainConflicts,
                                goodsTrainCount,
                                false
                        );

                score += dueDateScore(
                        task,
                        request.date()
                );

                score += goodsTrainScore(
                        goodsTrainCount
                );

                List<MaintenanceTask> coordinatedTasks =
                        findCoordinatedTasks(
                                request,
                                currentStart,
                                currentEnd
                        );

                score += coordinatedTasks.size() * 5.0;

                score = Math.max(
                        0.0,
                        Math.min(100.0, score)
                );

                candidates.add(
                        new CandidateBlock(
                                currentStart,
                                currentEnd,
                                score,
                                optimizationService
                                        .calculateTrainImpact(
                                                trainConflicts
                                        ),
                                trainConflicts,
                                goodsTrainCount,
                                coordinatedTasks
                        )
                );
            }

            currentStart =
                    currentStart.plusMinutes(15);
        }

        return candidates;
    }

    private MaintenancePlan saveOrUpdatePlan(
            MaintenancePlan existingPlan,
            MaintenanceTask task,
            BlockPlanRequest request,
            int duration,
            CandidateBlock best) {

        MaintenancePlan plan =
                existingPlan != null
                        ? existingPlan
                        : new MaintenancePlan();

        plan.setTaskId(task.getTaskId());
        plan.setCorridorId(request.corridorId());
        plan.setDepartment(task.getDepartment());
        plan.setDate(request.date());
        plan.setStartTime(best.startTime());
        plan.setEndTime(best.endTime());
        plan.setDuration(duration);
        plan.setPriority(request.priority());
        plan.setTrainImpact(best.trainImpact());
        plan.setStatus("PLANNED");

        return planRepository.save(plan);
    }

    private double calculateExistingPlanScore(
            MaintenanceTask task,
            Corridor corridor,
            MaintenancePlan plan) {

        int trainConflicts =
                conflictDetectionService
                        .countTrainConflicts(
                                plan.getCorridorId(),
                                plan.getStartTime(),
                                plan.getEndTime()
                        );

        int goodsTrainCount =
                goodsTrainForecastService
                        .getOverlappingGoodsTrainCount(
                                plan.getCorridorId(),
                                plan.getDate(),
                                plan.getStartTime(),
                                plan.getEndTime()
                        );

        return Math.max(
                0.0,
                Math.min(
                        100.0,
                        optimizationService.calculateScore(
                                task,
                                corridor,
                                trainConflicts,
                                goodsTrainCount,
                                false
                        )
                                + dueDateScore(
                                task,
                                plan.getDate()
                        )
                )
        );
    }

    private double dueDateScore(
            MaintenanceTask task,
            LocalDate planningDate) {

        if (task.getDueDate() == null
                || planningDate == null) {
            return 0.0;
        }

        long days =
                ChronoUnit.DAYS.between(
                        planningDate,
                        task.getDueDate()
                );

        if (days < 0) {
            return 20.0;
        }

        if (days == 0) {
            return 18.0;
        }

        if (days <= 2) {
            return 12.0;
        }

        if (days <= 7) {
            return 7.0;
        }

        return 2.0;
    }

    private double goodsTrainScore(
            int goodsTrainCount) {

        if (goodsTrainCount <= 0) {
            return 5.0;
        }

        if (goodsTrainCount == 1) {
            return 2.0;
        }

        return 0.0;
    }

    private List<MaintenanceTask> findCoordinatedTasks(
            BlockPlanRequest request,
            LocalTime start,
            LocalTime end) {

        return taskRepository.findAll()
                .stream()
                .filter(task ->
                        isPending(task))
                .filter(task ->
                        task.getLocation() != null
                                &&
                                task.getLocation()
                                        .equalsIgnoreCase(
                                                request.corridorId()
                                        ))
                .filter(task ->
                        task.getDepartment() != null
                                &&
                                request.department() != null
                                &&
                                !task.getDepartment()
                                        .equalsIgnoreCase(
                                                request.department()
                                        ))
                .toList();
    }

    private boolean isPending(
            MaintenanceTask task) {

        return task.getStatus() != null
                &&
                task.getStatus()
                        .equalsIgnoreCase("PENDING");
    }

    private boolean isHistorical(
            String status) {

        if (status == null) {
            return false;
        }

        return status.equalsIgnoreCase("COMPLETED")
                ||
                status.equalsIgnoreCase("CANCELLED");
    }

    private void validateCorridor(
            Corridor corridor) {

        if (corridor == null) {
            throw new IllegalArgumentException(
                    "Corridor not found."
            );
        }

        if (corridor.getAvailableStart() == null
                || corridor.getAvailableEnd() == null) {

            throw new IllegalArgumentException(
                    "Corridor availability window is not configured."
            );
        }

        if (corridor.getAvailableEnd()
                .isBefore(
                        corridor.getAvailableStart()
                )
                ||
                corridor.getAvailableEnd()
                        .equals(
                                corridor.getAvailableStart()
                        )) {

            throw new IllegalArgumentException(
                    "Invalid corridor availability window."
            );
        }

        if (corridor.getStatus() != null
                &&
                !corridor.getStatus()
                        .equalsIgnoreCase("AVAILABLE")) {

            throw new IllegalArgumentException(
                    "Corridor is not available for maintenance."
            );
        }
    }

    private int resolveDuration(
            BlockPlanRequest request,
            MaintenanceTask task) {

        if (request.duration() != null
                && request.duration() > 0) {

            return request.duration();
        }

        if (task.getEstimatedDuration() != null
                && task.getEstimatedDuration() > 0) {

            return task.getEstimatedDuration();
        }

        throw new IllegalArgumentException(
                "Maintenance duration is required."
        );
    }

    private String buildReason(
            MaintenanceTask task,
            Corridor corridor,
            CandidateBlock candidate) {

        return "Block selected using maintenance priority, "
                + "criticality "
                + task.getCriticality()
                + ", urgency "
                + task.getUrgency()
                + ", asset importance "
                + task.getAssetImportance()
                + ". Corridor availability is "
                + corridor.getAvailabilityPercent()
                + "%. Passenger train conflicts: "
                + candidate.trainConflicts()
                + ". Goods train forecast: "
                + candidate.goodsTrainCount()
                + ".";
    }

    private record CandidateBlock(
            LocalTime startTime,
            LocalTime endTime,
            double score,
            String trainImpact,
            int trainConflicts,
            int goodsTrainCount,
            List<MaintenanceTask> coordinatedTasks) {
    }
}