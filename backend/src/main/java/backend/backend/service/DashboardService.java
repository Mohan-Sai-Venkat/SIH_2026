package backend.backend.service;

import backend.backend.dto.DashboardResponse;
import backend.backend.model.Corridor;
import backend.backend.model.MaintenancePlan;
import backend.backend.model.MaintenanceTask;
import backend.backend.repository.CorridorRepository;
import backend.backend.repository.MaintenancePlanRepository;
import backend.backend.repository.MaintenanceTaskRepository;
import org.springframework.stereotype.Service;

import java.time.LocalDate;
import java.util.List;

@Service
public class DashboardService {

    private final MaintenanceTaskRepository maintenanceTaskRepository;
    private final MaintenancePlanRepository maintenancePlanRepository;
    private final CorridorRepository corridorRepository;

    public DashboardService(
            MaintenanceTaskRepository maintenanceTaskRepository,
            MaintenancePlanRepository maintenancePlanRepository,
            CorridorRepository corridorRepository) {

        this.maintenanceTaskRepository =
                maintenanceTaskRepository;

        this.maintenancePlanRepository =
                maintenancePlanRepository;

        this.corridorRepository =
                corridorRepository;
    }

    public DashboardResponse getDashboard() {

        List<MaintenanceTask> tasks =
                maintenanceTaskRepository.findAll();

        List<Corridor> corridors =
                corridorRepository.findAll();

        LocalDate today =
                LocalDate.now();

        List<MaintenancePlan> todayPlans =
                maintenancePlanRepository.findByDateBetween(
                        today,
                        today
                );

        long totalTasks =
                tasks.size();

        long pendingTasks =
                tasks.stream()
                        .filter(this::isActive)
                        .count();

        /*
         * Count active tasks whose actual priority is CRITICAL.
         * The database stores the value in the priority field.
         */
        long criticalTasks =
                tasks.stream()
                        .filter(this::isActive)
                        .filter(task ->
                                "CRITICAL".equalsIgnoreCase(
                                        task.getPriority()
                                ))
                        .count();

        long completedTasks =
                tasks.stream()
                        .filter(task ->
                                task.getStatus() != null
                                        &&
                                        task.getStatus()
                                                .equalsIgnoreCase(
                                                        "Completed"
                                                ))
                        .count();

        double averageAvailability =
                corridors.stream()
                        .filter(corridor ->
                                corridor
                                        .getAvailabilityPercent()
                                        != null)
                        .mapToDouble(
                                Corridor::getAvailabilityPercent
                        )
                        .average()
                        .orElse(0.0);

        int totalPlannedMinutes =
                todayPlans.stream()
                        .filter(plan ->
                                plan.getDuration() != null)
                        .mapToInt(
                                MaintenancePlan::getDuration
                        )
                        .sum();

        double blockUtilization =
                calculateBlockUtilization(
                        totalPlannedMinutes,
                        corridors
                );

        return new DashboardResponse(
                totalTasks,
                pendingTasks,
                criticalTasks,
                completedTasks,
                round(averageAvailability),
                round(blockUtilization)
        );
    }

    private boolean isActive(
            MaintenanceTask task) {

        if (task.getStatus() == null) {
            return true;
        }

        return !task.getStatus()
                .equalsIgnoreCase("Completed")
                &&
                !task.getStatus()
                        .equalsIgnoreCase("Cancelled");
    }

    private double calculateBlockUtilization(
            int plannedMinutes,
            List<Corridor> corridors) {

        if (corridors.isEmpty()) {
            return 0.0;
        }

        int totalAvailableMinutes =
                corridors.stream()
                        .filter(corridor ->
                                corridor.getAvailableStart()
                                        != null
                                        &&
                                        corridor.getAvailableEnd()
                                                != null)
                        .mapToInt(corridor -> {

                            int start =
                                    corridor.getAvailableStart()
                                            .getHour() * 60
                                            +
                                            corridor.getAvailableStart()
                                                    .getMinute();

                            int end =
                                    corridor.getAvailableEnd()
                                            .getHour() * 60
                                            +
                                            corridor.getAvailableEnd()
                                                    .getMinute();

                            if (end <= start) {
                                return 0;
                            }

                            return end - start;
                        })
                        .sum();

        if (totalAvailableMinutes <= 0) {
            return 0.0;
        }

        return Math.min(
                100.0,
                plannedMinutes * 100.0
                        / totalAvailableMinutes
        );
    }

    private double round(double value) {
        return Math.round(value * 100.0) / 100.0;
    }
}