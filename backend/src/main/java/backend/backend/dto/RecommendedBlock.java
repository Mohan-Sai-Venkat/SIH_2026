package backend.backend.dto;

import java.time.LocalDate;

public record RecommendedBlock(
        String corridorId,
        LocalDate date,
        String startTime,
        String endTime,
        Integer duration,
        String trainImpact,
        Double utilization,
        String reason
) {
}