package backend.backend.model;

import jakarta.persistence.*;

@Entity
@Table(name = "block_requests")
public class BlockRequest {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    private String blockId;

    private String taskId;

    private String corridorId;

    private String requestedStart;

    private String requestedEnd;

    private Integer requestedDuration;

    private String department;

    private String requestStatus;

    public BlockRequest() {
    }

    public BlockRequest(
            Long id,
            String blockId,
            String taskId,
            String corridorId,
            String requestedStart,
            String requestedEnd,
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

    public String getRequestedStart() {
        return requestedStart;
    }

    public void setRequestedStart(String requestedStart) {
        this.requestedStart = requestedStart;
    }

    public String getRequestedEnd() {
        return requestedEnd;
    }

    public void setRequestedEnd(String requestedEnd) {
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
