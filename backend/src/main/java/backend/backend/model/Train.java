package backend.backend.model;

import jakarta.persistence.*;
import java.time.LocalTime;

@Entity
@Table(name = "trains")
public class Train {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    private String trainId;

    private String trainName;

    private String corridorId;

    private LocalTime arrivalTime;

    private LocalTime departureTime;

    private String trainType;

    private String priority;

    public Train() {
    }

    public Train(
            Long id,
            String trainId,
            String trainName,
            String corridorId,
            LocalTime arrivalTime,
            LocalTime departureTime,
            String trainType,
            String priority) {

        this.id = id;
        this.trainId = trainId;
        this.trainName = trainName;
        this.corridorId = corridorId;
        this.arrivalTime = arrivalTime;
        this.departureTime = departureTime;
        this.trainType = trainType;
        this.priority = priority;
    }

    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public String getTrainId() {
        return trainId;
    }

    public void setTrainId(String trainId) {
        this.trainId = trainId;
    }

    public String getTrainName() {
        return trainName;
    }

    public void setTrainName(String trainName) {
        this.trainName = trainName;
    }

    public String getCorridorId() {
        return corridorId;
    }

    public void setCorridorId(String corridorId) {
        this.corridorId = corridorId;
    }

    public LocalTime getArrivalTime() {
        return arrivalTime;
    }

    public void setArrivalTime(LocalTime arrivalTime) {
        this.arrivalTime = arrivalTime;
    }

    public LocalTime getDepartureTime() {
        return departureTime;
    }

    public void setDepartureTime(LocalTime departureTime) {
        this.departureTime = departureTime;
    }

    public String getTrainType() {
        return trainType;
    }

    public void setTrainType(String trainType) {
        this.trainType = trainType;
    }

    public String getPriority() {
        return priority;
    }

    public void setPriority(String priority) {
        this.priority = priority;
    }
}