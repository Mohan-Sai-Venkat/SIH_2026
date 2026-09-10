package backend.backend.model;

import jakarta.persistence.*;
import java.time.LocalTime;

@Entity
@Table(name = "corridors")
public class Corridor {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(name = "corridor_id", nullable = false, unique = true)
    private String corridorId;

    @Column(name = "from_station", nullable = false)
    private String fromStation;

    @Column(name = "to_station", nullable = false)
    private String toStation;

    @Column(name = "distance_km", nullable = false)
    private Double distanceKm;

    @Column(name = "availability_percent", nullable = false)
    private Double availabilityPercent;

    @Column(name = "available_start", nullable = false)
    private LocalTime availableStart;

    @Column(name = "available_end", nullable = false)
    private LocalTime availableEnd;

    @Column(name = "train_count", nullable = false)
    private Integer trainCount;

    @Column(nullable = false)
    private String status;

    public Corridor() {
    }

    public Corridor(
            Long id,
            String corridorId,
            String fromStation,
            String toStation,
            Double distanceKm,
            Double availabilityPercent,
            LocalTime availableStart,
            LocalTime availableEnd,
            Integer trainCount,
            String status) {

        this.id = id;
        this.corridorId = corridorId;
        this.fromStation = fromStation;
        this.toStation = toStation;
        this.distanceKm = distanceKm;
        this.availabilityPercent = availabilityPercent;
        this.availableStart = availableStart;
        this.availableEnd = availableEnd;
        this.trainCount = trainCount;
        this.status = status;
    }

    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public String getCorridorId() {
        return corridorId;
    }

    public void setCorridorId(String corridorId) {
        this.corridorId = corridorId;
    }

    public String getFromStation() {
        return fromStation;
    }

    public void setFromStation(String fromStation) {
        this.fromStation = fromStation;
    }

    public String getToStation() {
        return toStation;
    }

    public void setToStation(String toStation) {
        this.toStation = toStation;
    }

    public Double getDistanceKm() {
        return distanceKm;
    }

    public void setDistanceKm(Double distanceKm) {
        this.distanceKm = distanceKm;
    }

    public Double getAvailabilityPercent() {
        return availabilityPercent;
    }

    public void setAvailabilityPercent(Double availabilityPercent) {
        this.availabilityPercent = availabilityPercent;
    }

    public LocalTime getAvailableStart() {
        return availableStart;
    }

    public void setAvailableStart(LocalTime availableStart) {
        this.availableStart = availableStart;
    }

    public LocalTime getAvailableEnd() {
        return availableEnd;
    }

    public void setAvailableEnd(LocalTime availableEnd) {
        this.availableEnd = availableEnd;
    }

    public Integer getTrainCount() {
        return trainCount;
    }

    public void setTrainCount(Integer trainCount) {
        this.trainCount = trainCount;
    }

    public String getStatus() {
        return status;
    }

    public void setStatus(String status) {
        this.status = status;
    }
}