package backend.backend.service;

import backend.backend.model.BlockRequest;
import backend.backend.model.MaintenancePlan;
import backend.backend.model.Train;
import backend.backend.repository.BlockRequestRepository;
import backend.backend.repository.MaintenancePlanRepository;
import backend.backend.repository.TrainRepository;
import org.springframework.stereotype.Service;

import java.time.LocalDate;
import java.time.LocalDateTime;
import java.time.LocalTime;
import java.util.List;

@Service
public class ConflictDetectionService {

    private final MaintenancePlanRepository maintenancePlanRepository;
    private final BlockRequestRepository blockRequestRepository;
    private final TrainRepository trainRepository;

    public ConflictDetectionService(
            MaintenancePlanRepository maintenancePlanRepository,
            BlockRequestRepository blockRequestRepository,
            TrainRepository trainRepository) {

        this.maintenancePlanRepository = maintenancePlanRepository;
        this.blockRequestRepository = blockRequestRepository;
        this.trainRepository = trainRepository;
    }

    // =========================================================
    // MAINTENANCE PLAN CONFLICT
    // =========================================================

    public boolean hasMaintenanceConflict(
            String corridorId,
            LocalDate date,
            LocalTime startTime,
            LocalTime endTime) {

        return hasMaintenanceConflict(
                corridorId,
                date,
                startTime,
                endTime,
                null
        );
    }

    /*
     * Same check, but allows the current plan to be excluded.
     * This is required when validating an existing plan.
     */
    public boolean hasMaintenanceConflict(
            String corridorId,
            LocalDate date,
            LocalTime startTime,
            LocalTime endTime,
            Long excludedPlanId) {

        List<MaintenancePlan> plans =
                maintenancePlanRepository
                        .findByCorridorIdAndDate(
                                corridorId,
                                date
                        );

        for (MaintenancePlan plan : plans) {

            if (plan == null) {
                continue;
            }

            // Ignore the plan currently being validated
            if (excludedPlanId != null
                    && plan.getId() != null
                    && plan.getId().equals(excludedPlanId)) {

                continue;
            }

            // Historical plans do not block a new plan
            if (isHistorical(plan.getStatus())) {
                continue;
            }

            if (plan.getStartTime() == null
                    || plan.getEndTime() == null) {
                continue;
            }

            if (timeOverlaps(
                    startTime,
                    endTime,
                    plan.getStartTime(),
                    plan.getEndTime())) {

                return true;
            }
        }

        return false;
    }

    // =========================================================
    // BLOCK REQUEST CONFLICT
    // =========================================================

    public boolean hasBlockRequestConflict(
            String corridorId,
            LocalDate date,
            LocalTime startTime,
            LocalTime endTime) {

        List<BlockRequest> requests =
                blockRequestRepository
                        .findByCorridorId(corridorId);

        for (BlockRequest request : requests) {

            if (request == null) {
                continue;
            }

            if (request.getRequestedStart() == null
                    || request.getRequestedEnd() == null) {
                continue;
            }

            LocalDate requestDate =
                    request.getRequestedStart().toLocalDate();

            if (!date.equals(requestDate)) {
                continue;
            }

            if (isRejectedOrCancelled(
                    request.getRequestStatus())) {
                continue;
            }

            LocalTime requestStart =
                    request.getRequestedStart().toLocalTime();

            LocalTime requestEnd =
                    request.getRequestedEnd().toLocalTime();

            if (timeOverlaps(
                    startTime,
                    endTime,
                    requestStart,
                    requestEnd)) {

                return true;
            }
        }

        return false;
    }

    // =========================================================
    // TRAIN CONFLICT COUNT
    // =========================================================

    public int countTrainConflicts(
            String corridorId,
            LocalTime startTime,
            LocalTime endTime) {

        List<Train> trains =
                trainRepository.findByCorridorId(corridorId);

        int conflicts = 0;

        for (Train train : trains) {

            if (train == null) {
                continue;
            }

            if (train.getArrivalTime() == null
                    || train.getDepartureTime() == null) {
                continue;
            }

            if (timeOverlaps(
                    startTime,
                    endTime,
                    train.getArrivalTime(),
                    train.getDepartureTime())) {

                conflicts++;
            }
        }

        return conflicts;
    }

    // =========================================================
    // HIGH PRIORITY TRAIN CONFLICT COUNT
    // =========================================================

    public int countHighPriorityTrainConflicts(
            String corridorId,
            LocalTime startTime,
            LocalTime endTime) {

        List<Train> trains =
                trainRepository.findByCorridorId(corridorId);

        int conflicts = 0;

        for (Train train : trains) {

            if (train == null) {
                continue;
            }

            if (train.getArrivalTime() == null
                    || train.getDepartureTime() == null) {
                continue;
            }

            if (!isHighPriority(train.getPriority())) {
                continue;
            }

            if (timeOverlaps(
                    startTime,
                    endTime,
                    train.getArrivalTime(),
                    train.getDepartureTime())) {

                conflicts++;
            }
        }

        return conflicts;
    }

    // =========================================================
    // TRAIN CONFLICT CHECK
    // =========================================================

    public boolean hasTrainConflict(
            String corridorId,
            LocalTime startTime,
            LocalTime endTime) {

        return countTrainConflicts(
                corridorId,
                startTime,
                endTime
        ) > 0;
    }

    // =========================================================
    // TIME OVERLAP
    // =========================================================

    private boolean timeOverlaps(
            LocalTime start1,
            LocalTime end1,
            LocalTime start2,
            LocalTime end2) {

        if (start1 == null
                || end1 == null
                || start2 == null
                || end2 == null) {

            return false;
        }

        return start1.isBefore(end2)
                && start2.isBefore(end1);
    }

    // =========================================================
    // STATUS HELPERS
    // =========================================================

    private boolean isHistorical(String status) {

        if (status == null) {
            return false;
        }

        return status.equalsIgnoreCase("COMPLETED")
                || status.equalsIgnoreCase("BLOCK_RELEASED")
                || status.equalsIgnoreCase("RELEASED");
    }

    private boolean isRejectedOrCancelled(String status) {

        if (status == null) {
            return false;
        }

        return status.equalsIgnoreCase("REJECTED")
                || status.equalsIgnoreCase("CANCELLED")
                || status.equalsIgnoreCase("CANCELED");
    }

    private boolean isHighPriority(String priority) {

        if (priority == null) {
            return false;
        }

        return priority.equalsIgnoreCase("HIGH")
                || priority.equalsIgnoreCase("CRITICAL");
    }
}