package backend.backend.model;

import jakarta.persistence.*;
import java.time.LocalDate;
import java.time.LocalTime;

@Entity
@Table(name = "goods_train_forecasts")
public class GoodsTrainForecast {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    private String corridorId;

    private LocalDate forecastDate;

    private Integer expectedTrainCount;

    private LocalTime peakStart;

    private LocalTime peakEnd;

    private Double confidence;

    public GoodsTrainForecast() {
    }

    public GoodsTrainForecast(
            Long id,
            String corridorId,
            LocalDate forecastDate,
            Integer expectedTrainCount,
            LocalTime peakStart,
            LocalTime peakEnd,
            Double confidence) {

        this.id = id;
        this.corridorId = corridorId;
        this.forecastDate = forecastDate;
        this.expectedTrainCount = expectedTrainCount;
        this.peakStart = peakStart;
        this.peakEnd = peakEnd;
        this.confidence = confidence;
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

    public LocalDate getForecastDate() {
        return forecastDate;
    }

    public void setForecastDate(LocalDate forecastDate) {
        this.forecastDate = forecastDate;
    }

    public Integer getExpectedTrainCount() {
        return expectedTrainCount;
    }

    public void setExpectedTrainCount(Integer expectedTrainCount) {
        this.expectedTrainCount = expectedTrainCount;
    }

    public LocalTime getPeakStart() {
        return peakStart;
    }

    public void setPeakStart(LocalTime peakStart) {
        this.peakStart = peakStart;
    }

    public LocalTime getPeakEnd() {
        return peakEnd;
    }

    public void setPeakEnd(LocalTime peakEnd) {
        this.peakEnd = peakEnd;
    }

    public Double getConfidence() {
        return confidence;
    }

    public void setConfidence(Double confidence) {
        this.confidence = confidence;
    }
}
