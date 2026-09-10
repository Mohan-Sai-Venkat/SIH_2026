package backend.backend.repository;

import backend.backend.model.MaintenancePlan;
import org.springframework.data.jpa.repository.JpaRepository;

import java.time.LocalDate;
import java.util.List;

public interface MaintenancePlanRepository
        extends JpaRepository<MaintenancePlan, Long> {

    List<MaintenancePlan> findByDateBetween(
            LocalDate start,
            LocalDate end
    );

    List<MaintenancePlan> findByCorridorIdAndDate(
            String corridorId,
            LocalDate date
    );

    List<MaintenancePlan> findByTaskId(
            String taskId
    );

    List<MaintenancePlan> findByDepartmentIgnoreCase(
            String department
    );

    boolean existsByTaskIdAndCorridorIdAndDate(
            String taskId,
            String corridorId,
            LocalDate date
    );
}