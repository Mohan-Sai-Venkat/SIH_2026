package backend.backend.controller;

import backend.backend.model.BlockRequest;
import backend.backend.repository.BlockRequestRepository;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.time.LocalDateTime;
import java.util.List;

@RestController
@RequestMapping("/api/block-requests")
@CrossOrigin(origins = "http://localhost:5173")
public class BlockPlanController {

    private final BlockRequestRepository repository;

    public BlockPlanController(BlockRequestRepository repository) {
        this.repository = repository;
    }

    // =========================================================
    // GET ALL
    // =========================================================

    @GetMapping
    public List<BlockRequest> getAllBlockRequests() {
        return repository.findAll();
    }

    // =========================================================
    // GET BY BLOCK ID
    // =========================================================

    @GetMapping("/{blockId}")
    public BlockRequest getBlockRequest(
            @PathVariable String blockId) {

        return repository.findByBlockId(blockId)
                .orElseThrow(() ->
                        new IllegalArgumentException(
                                "Block request not found: " + blockId));
    }

    // =========================================================
    // GET BY CORRIDOR
    // =========================================================

    @GetMapping("/corridor/{corridorId}")
    public List<BlockRequest> getByCorridor(
            @PathVariable String corridorId) {

        return repository.findByCorridorId(corridorId);
    }

    // =========================================================
    // GET BY TASK
    // =========================================================

    @GetMapping("/task/{taskId}")
    public List<BlockRequest> getByTask(
            @PathVariable String taskId) {

        return repository.findByTaskId(taskId);
    }

    // =========================================================
    // GET BY STATUS
    // =========================================================

    @GetMapping("/status/{status}")
    public List<BlockRequest> getByStatus(
            @PathVariable String status) {

        return repository.findByRequestStatusIgnoreCase(status);
    }

    // =========================================================
    // CREATE BLOCK REQUEST
    // REAL-TIME DUPLICATE + OVERLAP PROTECTION
    // =========================================================

    @PostMapping
    public ResponseEntity<?> createBlockRequest(
            @RequestBody BlockRequest request) {

        validateRequest(request);

        // -----------------------------------------------------
        // 1. EXACT DUPLICATE CHECK
        // -----------------------------------------------------

        boolean duplicate =
                repository
                        .findByTaskIdAndCorridorIdAndRequestedStartAndRequestedEnd(
                                request.getTaskId(),
                                request.getCorridorId(),
                                request.getRequestedStart(),
                                request.getRequestedEnd()
                        )
                        .isPresent();

        if (duplicate) {
            return ResponseEntity
                    .status(HttpStatus.CONFLICT)
                    .body("An active block request already exists for this task, corridor and time.");
        }

        // -----------------------------------------------------
        // 2. OVERLAPPING BLOCK CHECK
        // Different task but same corridor/time
        // -----------------------------------------------------

        List<BlockRequest> corridorRequests =
                repository.findByCorridorId(request.getCorridorId());

        for (BlockRequest existing : corridorRequests) {

            if (isInactive(existing.getRequestStatus())) {
                continue;
            }

            if (overlaps(
                    request.getRequestedStart(),
                    request.getRequestedEnd(),
                    existing.getRequestedStart(),
                    existing.getRequestedEnd())) {

                return ResponseEntity
                        .status(HttpStatus.CONFLICT)
                        .body(
                                "Block request conflicts with existing block "
                                        + existing.getBlockId()
                                        + " on corridor "
                                        + existing.getCorridorId()
                                        + "."
                        );
            }
        }

        // -----------------------------------------------------
        // 3. SAVE
        // -----------------------------------------------------

        try {

            BlockRequest saved = repository.save(request);

            return ResponseEntity
                    .status(HttpStatus.CREATED)
                    .body(saved);

        } catch (org.springframework.dao.DataIntegrityViolationException ex) {

            // Database unique constraint is the final protection
            return ResponseEntity
                    .status(HttpStatus.CONFLICT)
                    .body(
                            "Duplicate block request rejected by database protection."
                    );
        }
    }

    // =========================================================
    // VALIDATION
    // =========================================================

    private void validateRequest(BlockRequest request) {

        if (request == null) {
            throw new IllegalArgumentException(
                    "Block request is required.");
        }

        if (request.getBlockId() == null
                || request.getBlockId().isBlank()) {

            throw new IllegalArgumentException(
                    "Block ID is required.");
        }

        if (request.getTaskId() == null
                || request.getTaskId().isBlank()) {

            throw new IllegalArgumentException(
                    "Task ID is required.");
        }

        if (request.getCorridorId() == null
                || request.getCorridorId().isBlank()) {

            throw new IllegalArgumentException(
                    "Corridor ID is required.");
        }

        if (request.getRequestedStart() == null) {

            throw new IllegalArgumentException(
                    "Requested start time is required.");
        }

        if (request.getRequestedEnd() == null) {

            throw new IllegalArgumentException(
                    "Requested end time is required.");
        }

        if (!request.getRequestedStart()
                .isBefore(request.getRequestedEnd())) {

            throw new IllegalArgumentException(
                    "Requested start time must be before requested end time.");
        }

        if (request.getRequestedDuration() == null
                || request.getRequestedDuration() <= 0) {

            throw new IllegalArgumentException(
                    "Requested duration must be greater than zero.");
        }

        if (request.getDepartment() == null
                || request.getDepartment().isBlank()) {

            throw new IllegalArgumentException(
                    "Department is required.");
        }

        if (request.getRequestStatus() == null
                || request.getRequestStatus().isBlank()) {

            request.setRequestStatus("PENDING");
        }
    }

    // =========================================================
    // OVERLAP CHECK
    // =========================================================

    private boolean overlaps(
            LocalDateTime start1,
            LocalDateTime end1,
            LocalDateTime start2,
            LocalDateTime end2) {

        if (start1 == null || end1 == null
                || start2 == null || end2 == null) {

            return false;
        }

        return start1.isBefore(end2)
                && end1.isAfter(start2);
    }

    // =========================================================
    // INACTIVE REQUESTS DO NOT BLOCK NEW REQUESTS
    // =========================================================

    private boolean isInactive(String status) {

        if (status == null) {
            return false;
        }

        return status.equalsIgnoreCase("REJECTED")
                || status.equalsIgnoreCase("CANCELLED")
                || status.equalsIgnoreCase("CANCELED")
                || status.equalsIgnoreCase("RELEASED")
                || status.equalsIgnoreCase("BLOCK_RELEASED")
                || status.equalsIgnoreCase("COMPLETED");
    }
}