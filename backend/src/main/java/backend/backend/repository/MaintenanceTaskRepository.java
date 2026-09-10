package backend.backend.repository;

import backend.backend.model.MaintenanceTask;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;
import java.util.Optional;

public interface MaintenanceTaskRepository
        extends JpaRepository<MaintenanceTask, Long> {

    Optional<MaintenanceTask> findByTaskId(String taskId);

    List<MaintenanceTask> findByDepartmentIgnoreCase(
            String department
    );

    List<MaintenanceTask> findByStatusIgnoreCase(
            String status
    );

    List<MaintenanceTask> findByCriticalityIgnoreCase(
            String criticality
    );
}