package backend.backend.repository;

import backend.backend.model.BlockRequest;
import org.springframework.data.jpa.repository.JpaRepository;

import java.time.LocalDateTime;
import java.util.List;
import java.util.Optional;

public interface BlockRequestRepository
        extends JpaRepository<BlockRequest, Long> {

    List<BlockRequest> findByCorridorId(String corridorId);

    List<BlockRequest> findByTaskId(String taskId);

    List<BlockRequest> findByRequestStatusIgnoreCase(String requestStatus);

    Optional<BlockRequest> findByBlockId(String blockId);

    Optional<BlockRequest> findByTaskIdAndCorridorIdAndRequestedStartAndRequestedEnd(
            String taskId,
            String corridorId,
            LocalDateTime requestedStart,
            LocalDateTime requestedEnd
    );
}