package backend.backend.controller;

import backend.backend.model.MaintenanceTask;
import backend.backend.service.MaintenanceService;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/maintenance")
public class MaintenanceController {

    private final MaintenanceService service;

    public MaintenanceController(
            MaintenanceService service) {

        this.service = service;
    }

    @GetMapping
    public List<MaintenanceTask> getAll(
            @RequestParam(required = false)
            String department,

            @RequestParam(required = false)
            String status,

            @RequestParam(required = false)
            String criticality) {

        return service.getAll(
                department,
                status,
                criticality
        );
    }

    @GetMapping("/{taskId}")
    public MaintenanceTask getByTaskId(
            @PathVariable String taskId) {

        return service.getByTaskId(taskId);
    }

    @GetMapping("/pending")
    public List<MaintenanceTask> getPendingTasks() {
        return service.getPendingTasks();
    }

    @GetMapping("/pending/{department}")
    public List<MaintenanceTask>
    getPendingTasksByDepartment(
            @PathVariable String department) {

        return service.getPendingTasksByDepartment(
                department
        );
    }

    @PostMapping
    @ResponseStatus(HttpStatus.CREATED)
    public MaintenanceTask create(
            @RequestBody MaintenanceTask task) {

        return service.create(task);
    }

    @PutMapping("/{taskId}")
    public MaintenanceTask update(
            @PathVariable String taskId,
            @RequestBody MaintenanceTask task) {

        return service.update(
                taskId,
                task
        );
    }

    @DeleteMapping("/{taskId}")
    @ResponseStatus(HttpStatus.NO_CONTENT)
    public void delete(
            @PathVariable String taskId) {

        service.delete(taskId);
    }
}