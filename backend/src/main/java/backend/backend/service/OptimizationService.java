package backend.backend.service;

import backend.backend.model.Corridor;
import backend.backend.model.MaintenanceTask;
import org.springframework.stereotype.Service;

@Service
public class OptimizationService {

    public double calculateScore(
            MaintenanceTask task,
            Corridor corridor,
            int trainConflicts,
            int goodsTrainCount,
            boolean maintenanceConflict) {

        double score = 50.0;

        score += getCriticalityScore(
                task.getCriticality()
        );

        score += getUrgencyScore(
                task.getUrgency()
        );

        score += getAssetImportanceScore(
                task.getAssetImportance()
        );

        if (corridor != null) {
            score += getCorridorAvailabilityScore(
                    corridor.getAvailabilityPercent()
            );
        }

        score -= trainConflicts * 10.0;

        score -= goodsTrainCount * 4.0;

        if (maintenanceConflict) {
            score -= 100.0;
        }

        return Math.max(
                0.0,
                Math.min(100.0, score)
        );
    }

    private double getCriticalityScore(
            String criticality) {

        if (criticality == null) {
            return 0.0;
        }

        return switch (
                criticality.trim().toLowerCase()) {

            case "critical" -> 25.0;
            case "high" -> 20.0;
            case "medium" -> 12.0;
            case "low" -> 5.0;
            default -> 0.0;
        };
    }

    private double getUrgencyScore(
            String urgency) {

        if (urgency == null) {
            return 0.0;
        }

        return switch (
                urgency.trim().toLowerCase()) {

            case "critical" -> 20.0;
            case "high" -> 15.0;
            case "medium" -> 10.0;
            case "low" -> 5.0;
            default -> 0.0;
        };
    }

    private double getAssetImportanceScore(
            Integer assetImportance) {

        if (assetImportance == null) {
            return 0.0;
        }

        return Math.min(
                20.0,
                Math.max(0, assetImportance) * 0.75
        );
    }

    private double getCorridorAvailabilityScore(
            Double availabilityPercent) {

        if (availabilityPercent == null) {
            return 0.0;
        }

        return Math.max(
                0.0,
                Math.min(
                        20.0,
                        availabilityPercent * 0.20
                )
        );
    }

    public String calculateTrainImpact(
            int trainConflicts) {

        if (trainConflicts <= 0) {
            return "Low";
        }

        if (trainConflicts == 1) {
            return "Medium";
        }

        return "High";
    }
}