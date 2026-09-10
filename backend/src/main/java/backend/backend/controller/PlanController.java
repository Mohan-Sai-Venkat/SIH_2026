package backend.backend.controller;

import backend.backend.dto.BlockPlanRequest;
import backend.backend.dto.BlockPlanResponse;
import backend.backend.model.MaintenancePlan;
import backend.backend.repository.MaintenancePlanRepository;
import backend.backend.service.PlanService;
import org.springframework.web.bind.annotation.*;

import java.time.LocalDate;
import java.util.List;

@RestController
@RequestMapping("/api/plans")
public class PlanController {

    private final PlanService planService;
    private final MaintenancePlanRepository planRepository;

    public PlanController(
            PlanService planService,
            MaintenancePlanRepository planRepository) {

        this.planService = planService;
        this.planRepository = planRepository;
    }

    @PostMapping("/generate")
    public BlockPlanResponse generatePlan(
            @RequestBody BlockPlanRequest request) {

        return planService.generatePlan(request);
    }

    @GetMapping
    public List<MaintenancePlan> getPlans(
            @RequestParam(required = false) LocalDate date) {

        if (date != null) {
            return planRepository.findByDateBetween(
                    date,
                    date
            );
        }

        return planRepository.findAll();
    }

    @GetMapping("/weekly")
    public List<MaintenancePlan> getWeeklyPlans() {

        LocalDate startDate = LocalDate.now();
        LocalDate endDate = startDate.plusDays(7);

        return planRepository.findByDateBetween(
                startDate,
                endDate
        );
    }

    @GetMapping("/monthly")
    public List<MaintenancePlan> getMonthlyPlans() {

        LocalDate startDate = LocalDate.now();
        LocalDate endDate = startDate.plusDays(30);

        return planRepository.findByDateBetween(
                startDate,
                endDate
        );
    }

    @GetMapping("/{id}")
    public MaintenancePlan getPlanById(
            @PathVariable Long id) {

        return planRepository.findById(id)
                .orElseThrow(() ->
                        new IllegalArgumentException(
                                "Maintenance plan not found: " + id
                        ));
    }
}