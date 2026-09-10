package backend.backend.service;

import backend.backend.dto.BlockPlanRequest;
import backend.backend.dto.BlockPlanResponse;
import org.springframework.stereotype.Service;

@Service
public class BlockPlanningService {

    private final PlanService planService;

    public BlockPlanningService(PlanService planService) {
        this.planService = planService;
    }

    public BlockPlanResponse generatePlan(BlockPlanRequest request) {
        return planService.generatePlan(request);
    }
}