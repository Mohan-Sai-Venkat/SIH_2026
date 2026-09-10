package backend.backend.service;

import backend.backend.model.MaintenanceTask;
import backend.backend.repository.MaintenanceTaskRepository;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class MaintenanceService {

    private final MaintenanceTaskRepository repository;

    public MaintenanceService(MaintenanceTaskRepository repository) {
        this.repository = repository;
    }

    public List<MaintenanceTask> getAll(
            String department,
            String status,
            String criticality) {

        List<MaintenanceTask> tasks = repository.findAll();

        return tasks.stream()
                .filter(task ->
                        department == null ||
                                department.isBlank() ||
                                (task.getDepartment() != null &&
                                        task.getDepartment()
                                                .equalsIgnoreCase(department)))
                .filter(task ->
                        status == null ||
                                status.isBlank() ||
                                (task.getStatus() != null &&
                                        task.getStatus()
                                                .equalsIgnoreCase(status)))
                .filter(task ->
                        criticality == null ||
                                criticality.isBlank() ||
                                (task.getCriticality() != null &&
                                        task.getCriticality()
                                                .equalsIgnoreCase(criticality)))
                .toList();
    }

    public MaintenanceTask getByTaskId(String taskId) {

        if (taskId == null || taskId.isBlank()) {
            throw new IllegalArgumentException(
                    "Task ID is required."
            );
        }

        return repository.findByTaskId(taskId)
                .orElseThrow(() ->
                        new IllegalArgumentException(
                                "Maintenance task not found: " + taskId
                        ));
    }

    public List<MaintenanceTask> getPendingTasks() {
        return repository.findByStatusIgnoreCase("PENDING");
    }

    public List<MaintenanceTask> getPendingTasksByDepartment(
            String department) {

        return repository
                .findByDepartmentIgnoreCase(department)
                .stream()
                .filter(task ->
                        task.getStatus() != null &&
                                task.getStatus()
                                        .equalsIgnoreCase("PENDING"))
                .toList();
    }

    public MaintenanceTask create(MaintenanceTask task) {

        if (task == null) {
            throw new IllegalArgumentException(
                    "Maintenance task cannot be null."
            );
        }

        if (task.getTaskId() == null ||
                task.getTaskId().isBlank()) {
            throw new IllegalArgumentException(
                    "Task ID is required."
            );
        }

        if (repository.findByTaskId(task.getTaskId()).isPresent()) {
            throw new IllegalArgumentException(
                    "Maintenance task already exists: "
                            + task.getTaskId()
            );
        }

        if (task.getAssetId() == null ||
                task.getAssetId().isBlank()) {
            throw new IllegalArgumentException(
                    "Asset ID is required."
            );
        }

        if (task.getDepartment() == null ||
                task.getDepartment().isBlank()) {
            throw new IllegalArgumentException(
                    "Department is required."
            );
        }

        if (task.getLocation() == null ||
                task.getLocation().isBlank()) {
            throw new IllegalArgumentException(
                    "Location is required."
            );
        }

        if (task.getEstimatedDuration() == null ||
                task.getEstimatedDuration() <= 0) {
            throw new IllegalArgumentException(
                    "Estimated duration must be greater than zero."
            );
        }

        if (task.getStatus() == null ||
                task.getStatus().isBlank()) {
            task.setStatus("PENDING");
        }

        if (task.getPriority() == null ||
                task.getPriority().isBlank()) {
            task.setPriority("MEDIUM");
        }

        if (task.getSafetyImpact() == null) {
            task.setSafetyImpact(false);
        }

        if (task.getBlockRequired() == null) {
            task.setBlockRequired(true);
        }

        return repository.save(task);
    }

    public MaintenanceTask update(
            String taskId,
            MaintenanceTask updatedTask) {

        MaintenanceTask existing =
                getByTaskId(taskId);

        if (updatedTask.getAssetId() != null) {
            existing.setAssetId(
                    updatedTask.getAssetId()
            );
        }

        if (updatedTask.getDepartment() != null) {
            existing.setDepartment(
                    updatedTask.getDepartment()
            );
        }

        if (updatedTask.getLocation() != null) {
            existing.setLocation(
                    updatedTask.getLocation()
            );
        }

        if (updatedTask.getDefect() != null) {
            existing.setDefect(
                    updatedTask.getDefect()
            );
        }

        if (updatedTask.getEstimatedDuration() != null) {
            if (updatedTask.getEstimatedDuration() <= 0) {
                throw new IllegalArgumentException(
                        "Estimated duration must be greater than zero."
                );
            }

            existing.setEstimatedDuration(
                    updatedTask.getEstimatedDuration()
            );
        }

        if (updatedTask.getDate() != null) {
            existing.setDate(
                    updatedTask.getDate()
            );
        }

        if (updatedTask.getStatus() != null) {
            existing.setStatus(
                    updatedTask.getStatus()
            );
        }

        if (updatedTask.getPriority() != null) {
            existing.setPriority(
                    updatedTask.getPriority()
            );
        }

        if (updatedTask.getPriorityScore() != null) {
            existing.setPriorityScore(
                    updatedTask.getPriorityScore()
            );
        }

        if (updatedTask.getSafetyImpact() != null) {
            existing.setSafetyImpact(
                    updatedTask.getSafetyImpact()
            );
        }

        if (updatedTask.getTrainTraffic() != null) {
            existing.setTrainTraffic(
                    updatedTask.getTrainTraffic()
            );
        }

        if (updatedTask.getOverdueDays() != null) {
            existing.setOverdueDays(
                    updatedTask.getOverdueDays()
            );
        }

        if (updatedTask.getSourceSystem() != null) {
            existing.setSourceSystem(
                    updatedTask.getSourceSystem()
            );
        }

        if (updatedTask.getBlockRequired() != null) {
            existing.setBlockRequired(
                    updatedTask.getBlockRequired()
            );
        }

        if (updatedTask.getWorkerId() != null) {
            existing.setWorkerId(
                    updatedTask.getWorkerId()
            );
        }

        if (updatedTask.getWorkerName() != null) {
            existing.setWorkerName(
                    updatedTask.getWorkerName()
            );
        }

        if (updatedTask.getCriticality() != null) {
            existing.setCriticality(
                    updatedTask.getCriticality()
            );
        }

        if (updatedTask.getUrgency() != null) {
            existing.setUrgency(
                    updatedTask.getUrgency()
            );
        }

        if (updatedTask.getAssetImportance() != null) {
            existing.setAssetImportance(
                    updatedTask.getAssetImportance()
            );
        }

        return repository.save(existing);
    }

    public void delete(String taskId) {
        MaintenanceTask task =
                getByTaskId(taskId);

        repository.delete(task);
    }
}