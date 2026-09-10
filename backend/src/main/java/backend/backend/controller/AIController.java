package backend.backend.controller;

import backend.backend.dto.AIBlockPlanRequest;
import backend.backend.dto.AIInsightResponse;
import backend.backend.dto.BlockPlanRequest;
import backend.backend.dto.BlockPlanResponse;
import backend.backend.service.AIService;
import backend.backend.service.BlockPlanningService;
import jakarta.validation.Valid;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/ai")
public class AIController {

    private final AIService aiService;
    private final BlockPlanningService blockPlanningService;

    public AIController(
            AIService aiService,
            BlockPlanningService blockPlanningService) {

        this.aiService = aiService;
        this.blockPlanningService = blockPlanningService;
    }

    @GetMapping("/insights")
    public List<AIInsightResponse> getInsights() {
        return aiService.generateInsights();
    }

    @PostMapping("/block-plan")
    public BlockPlanResponse generateBlockPlan(
            @Valid @RequestBody BlockPlanRequest request) {

        return blockPlanningService.generatePlan(request);
    }

    @PostMapping("/generate")
    public BlockPlanResponse generateAIBlockPlan(
            @Valid @RequestBody AIBlockPlanRequest request) {

        BlockPlanRequest blockPlanRequest =
                new BlockPlanRequest(
                        request.date(),
                        request.corridorId(),
                        request.department(),
                        request.duration(),
                        request.priority(),
                        request.taskId()
                );

        return blockPlanningService.generatePlan(
                blockPlanRequest
        );
    }
}