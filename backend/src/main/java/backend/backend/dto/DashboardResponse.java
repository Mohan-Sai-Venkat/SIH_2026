package backend.backend.dto;

public record DashboardResponse(
        long totalTasks,
        long pendingTasks,
        long criticalTasks,
        long completedTasks,
        double averageAvailability,
        double blockUtilization
) {
}