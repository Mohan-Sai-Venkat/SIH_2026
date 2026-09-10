package backend.backend.dto;

import java.util.List;

public record BlockPlanResponse(
        boolean success,
        RecommendedBlock recommendedBlock,
        List<AlternativeBlock> alternatives
) {
}