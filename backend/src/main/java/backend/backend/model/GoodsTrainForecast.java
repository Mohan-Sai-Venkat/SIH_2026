package backend.backend.model;

import jakarta.persistence.*;
import lombok.*;

import java.time.LocalDate;
import java.time.LocalTime;

@Entity
@Table(name = "goods_train_forecasts")
@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class GoodsTrainForecast {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(name = "corridor_id", nullable = false)
    private String corridorId;

    @Column(name = "forecast_date", nullable = false)
    private LocalDate forecastDate;

    @Column(name = "expected_train_count", nullable = false)
    private Integer expectedTrainCount;

    @Column(name = "peak_start")
    private LocalTime peakStart;

    @Column(name = "peak_end")
    private LocalTime peakEnd;

    @Column(nullable = false)
    private Double confidence;
}