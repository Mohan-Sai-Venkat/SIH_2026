package backend.backend.model;

import jakarta.persistence.*;

import java.time.LocalDate;

@Entity
@Table(name = "maintenance_task")
public class MaintenanceTask {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(name = "task_id", nullable = false, unique = true)
    private String taskId;

    @Column(name = "asset_id")
    private String assetId;

    @Column(name = "location")
    private String location;

    @Column(name = "department")
    private String department;

    @Column(name = "defect")
    private String defect;

    @Column(name = "duration")
    private Integer estimatedDuration;

    @Column(name = "date")
    private LocalDate date;

    @Column(name = "status")
    private String status;

    @Column(name = "priority")
    private String priority;

    @Column(name = "priority_score")
    private Integer priorityScore;

    @Column(name = "safety_impact")
    private Boolean safetyImpact;

    @Column(name = "train_traffic")
    private Integer trainTraffic;

    @Column(name = "overdue_days")
    private Integer overdueDays;

    @Column(name = "source_system")
    private String sourceSystem;

    @Column(name = "block_required")
    private Boolean blockRequired;

    @Column(name = "worker_id")
    private String workerId;

    @Column(name = "worker_name")
    private String workerName;

    @Transient
    private String criticality;

    @Transient
    private String urgency;

    @Transient
    private Integer assetImportance;

    public MaintenanceTask() {
    }

    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public String getTaskId() {
        return taskId;
    }

    public void setTaskId(String taskId) {
        this.taskId = taskId;
    }

    public String getAssetId() {
        return assetId;
    }

    public void setAssetId(String assetId) {
        this.assetId = assetId;
    }

    public String getLocation() {
        return location;
    }

    public void setLocation(String location) {
        this.location = location;
    }

    public String getDepartment() {
        return department;
    }

    public void setDepartment(String department) {
        this.department = department;
    }

    public String getDefect() {
        return defect;
    }

    public void setDefect(String defect) {
        this.defect = defect;
    }

    public Integer getEstimatedDuration() {
        return estimatedDuration;
    }

    public void setEstimatedDuration(Integer estimatedDuration) {
        this.estimatedDuration = estimatedDuration;
    }

    public LocalDate getDate() {
        return date;
    }

    public void setDate(LocalDate date) {
        this.date = date;
    }

    public LocalDate getDueDate() {
        return date;
    }

    public void setDueDate(LocalDate dueDate) {
        this.date = dueDate;
    }

    public String getStatus() {
        return status;
    }

    public void setStatus(String status) {
        this.status = status;
    }

    public String getPriority() {
        return priority;
    }

    public void setPriority(String priority) {
        this.priority = priority;
    }

    public Integer getPriorityScore() {
        return priorityScore;
    }

    public void setPriorityScore(Integer priorityScore) {
        this.priorityScore = priorityScore;
    }

    public Boolean getSafetyImpact() {
        return safetyImpact;
    }

    public void setSafetyImpact(Boolean safetyImpact) {
        this.safetyImpact = safetyImpact;
    }

    public Integer getTrainTraffic() {
        return trainTraffic;
    }

    public void setTrainTraffic(Integer trainTraffic) {
        this.trainTraffic = trainTraffic;
    }

    public Integer getOverdueDays() {
        return overdueDays;
    }

    public void setOverdueDays(Integer overdueDays) {
        this.overdueDays = overdueDays;
    }

    public String getSourceSystem() {
        return sourceSystem;
    }

    public void setSourceSystem(String sourceSystem) {
        this.sourceSystem = sourceSystem;
    }

    public Boolean getBlockRequired() {
        return blockRequired;
    }

    public void setBlockRequired(Boolean blockRequired) {
        this.blockRequired = blockRequired;
    }

    public String getWorkerId() {
        return workerId;
    }

    public void setWorkerId(String workerId) {
        this.workerId = workerId;
    }

    public String getWorkerName() {
        return workerName;
    }

    public void setWorkerName(String workerName) {
        this.workerName = workerName;
    }

    public String getCriticality() {
        return criticality;
    }

    public void setCriticality(String criticality) {
        this.criticality = criticality;
    }

    public String getUrgency() {
        return urgency;
    }

    public void setUrgency(String urgency) {
        this.urgency = urgency;
    }

    public Integer getAssetImportance() {
        return assetImportance;
    }

    public void setAssetImportance(Integer assetImportance) {
        this.assetImportance = assetImportance;
    }
}