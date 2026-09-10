package backend.backend.model;

import jakarta.persistence.*;
import java.time.LocalDateTime;

@Entity
@Table(name = "block_requests")
public class BlockRequest {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(name = "block_id", nullable = false, unique = true)
    private String blockId;

    @Column(name = "task_id", nullable = false)
    private String taskId;

    @Column(name = "corridor_id", nullable = false)
    private String corridorId;

    @Column(name = "requested_start", nullable = false)
    private LocalDateTime requestedStart;

    @Column(name = "requested_end", nullable = false)
    private LocalDateTime requestedEnd;

    @Column(name = "requested_duration", nullable = false)
    private Integer requestedDuration;

    @Column(nullable = false)
    private String department;

    @Column(name = "request_status", nullable = false)
    private String requestStatus;

    public BlockRequest() {
    }

    public BlockRequest(
            Long id,
            String blockId,
            String taskId,
            String corridorId,
            LocalDateTime requestedStart,
            LocalDateTime requestedEnd,
            Integer requestedDuration,
            String department,
            String requestStatus) {

        this.id = id;
        this.blockId = blockId;
        this.taskId = taskId;
        this.corridorId = corridorId;
        this.requestedStart = requestedStart;
        this.requestedEnd = requestedEnd;
        this.requestedDuration = requestedDuration;
        this.department = department;
        this.requestStatus = requestStatus;
    }

    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public String getBlockId() {
        return blockId;
    }

    public void setBlockId(String blockId) {
        this.blockId = blockId;
    }

    public String getTaskId() {
        return taskId;
    }

    public void setTaskId(String taskId) {
        this.taskId = taskId;
    }

    public String getCorridorId() {
        return corridorId;
    }

    public void setCorridorId(String corridorId) {
        this.corridorId = corridorId;
    }

    public LocalDateTime getRequestedStart() {
        return requestedStart;
    }

    public void setRequestedStart(LocalDateTime requestedStart) {
        this.requestedStart = requestedStart;
    }

    public LocalDateTime getRequestedEnd() {
        return requestedEnd;
    }

    public void setRequestedEnd(LocalDateTime requestedEnd) {
        this.requestedEnd = requestedEnd;
    }

    public Integer getRequestedDuration() {
        return requestedDuration;
    }

    public void setRequestedDuration(Integer requestedDuration) {
        this.requestedDuration = requestedDuration;
    }

    public String getDepartment() {
        return department;
    }

    public void setDepartment(String department) {
        this.department = department;
    }

    public String getRequestStatus() {
        return requestStatus;
    }

    public void setRequestStatus(String requestStatus) {
        this.requestStatus = requestStatus;
    }
}