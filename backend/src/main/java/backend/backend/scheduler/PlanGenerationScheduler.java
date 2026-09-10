package backend.backend.scheduler;

import backend.backend.model.MaintenanceTask;
import backend.backend.repository.MaintenanceTaskRepository;
import backend.backend.service.PlanService;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Component;

import java.time.LocalDate;
import java.util.List;

@Component
public class PlanGenerationScheduler {

    private final MaintenanceTaskRepository maintenanceTaskRepository;
    private final PlanService planService;

    public PlanGenerationScheduler(
            MaintenanceTaskRepository maintenanceTaskRepository,
            PlanService planService) {

        this.maintenanceTaskRepository = maintenanceTaskRepository;
        this.planService = planService;
    }

    @Scheduled(
            cron = "0 0 1 * * *",
            zone = "Asia/Kolkata"
    )
    public void dailyPlanningCheck() {

        LocalDate tomorrow = LocalDate.now().plusDays(1);

        List<MaintenanceTask> pendingTasks =
                maintenanceTaskRepository.findAll()
                        .stream()
                        .filter(task ->
                                task.getStatus() != null &&
                                        !task.getStatus()
                                                .equalsIgnoreCase("Completed") &&
                                        !task.getStatus()
                                                .equalsIgnoreCase("Cancelled"))
                        .filter(task ->
                                task.getEstimatedDuration() != null &&
                                        task.getEstimatedDuration() > 0)
                        .toList();

        System.out.println(
                "Daily railway maintenance planning cycle started for "
                        + tomorrow
        );

        System.out.println(
                "Pending maintenance tasks: "
                        + pendingTasks.size()
        );
    }
}