package backend.backend.service;

import backend.backend.dto.AIInsightResponse;
import backend.backend.model.Corridor;
import backend.backend.model.MaintenanceTask;
import backend.backend.repository.CorridorRepository;
import backend.backend.repository.MaintenanceTaskRepository;
import org.springframework.stereotype.Service;

import java.time.LocalDate;
import java.util.ArrayList;
import java.util.List;

@Service
public class AIService {

    private final MaintenanceTaskRepository maintenanceTaskRepository;
    private final CorridorRepository corridorRepository;

    public AIService(
            MaintenanceTaskRepository maintenanceTaskRepository,
            CorridorRepository corridorRepository) {

        this.maintenanceTaskRepository =
                maintenanceTaskRepository;

        this.corridorRepository =
                corridorRepository;
    }

    public List<AIInsightResponse> generateInsights() {

        List<AIInsightResponse> insights =
                new ArrayList<>();

        List<MaintenanceTask> tasks =
                maintenanceTaskRepository.findAll();

        List<Corridor> corridors =
                corridorRepository.findAll();

        long criticalTasks =
                tasks.stream()
                        .filter(this::isActive)
                        .filter(task ->
                                "Critical".equalsIgnoreCase(
                                        task.getCriticality()
                                ))
                        .count();

        long highUrgencyTasks =
                tasks.stream()
                        .filter(this::isActive)
                        .filter(task ->
                                "High".equalsIgnoreCase(
                                        task.getUrgency()
                                )
                                        ||
                                        "Critical".equalsIgnoreCase(
                                                task.getUrgency()
                                        ))
                        .count();

        long overdueTasks =
                tasks.stream()
                        .filter(this::isActive)
                        .filter(task ->
                                task.getDueDate() != null
                        )
                        .filter(task ->
                                task.getDueDate()
                                        .isBefore(
                                                LocalDate.now()
                                        ))
                        .count();

        long lowAvailabilityCorridors =
                corridors.stream()
                        .filter(corridor ->
                                corridor.getAvailabilityPercent() != null
                                        &&
                                        corridor.getAvailabilityPercent()
                                                < 90.0
                        )
                        .count();

        if (criticalTasks > 0) {
            insights.add(
                    new AIInsightResponse(
                            "Critical Maintenance",
                            criticalTasks
                                    + " critical maintenance task(s) require priority planning.",
                            "HIGH"
                    )
            );
        }

        if (highUrgencyTasks > 0) {
            insights.add(
                    new AIInsightResponse(
                            "Urgent Work",
                            highUrgencyTasks
                                    + " high-priority maintenance task(s) should be considered during block planning.",
                            "HIGH"
                    )
            );
        }

        if (overdueTasks > 0) {
            insights.add(
                    new AIInsightResponse(
                            "Overdue Maintenance",
                            overdueTasks
                                    + " pending maintenance task(s) are past their due date.",
                            "CRITICAL"
                    )
            );
        }

        if (lowAvailabilityCorridors > 0) {
            insights.add(
                    new AIInsightResponse(
                            "Corridor Availability",
                            lowAvailabilityCorridors
                                    + " corridor(s) have availability below 90%.",
                            "MEDIUM"
                    )
            );
        }

        if (insights.isEmpty()) {
            insights.add(
                    new AIInsightResponse(
                            "System Status",
                            "No immediate maintenance planning risks detected.",
                            "LOW"
                    )
            );
        }

        return insights;
    }

    private boolean isActive(
            MaintenanceTask task) {

        if (task.getStatus() == null) {
            return true;
        }

        return !task.getStatus()
                .equalsIgnoreCase("COMPLETED")
                &&
                !task.getStatus()
                        .equalsIgnoreCase("CANCELLED");
    }
}