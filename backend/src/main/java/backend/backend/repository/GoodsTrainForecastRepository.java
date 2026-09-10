package backend.backend.repository;

import backend.backend.model.GoodsTrainForecast;
import org.springframework.data.jpa.repository.JpaRepository;

import java.time.LocalDate;
import java.util.List;

public interface GoodsTrainForecastRepository
        extends JpaRepository<GoodsTrainForecast, Long> {

    List<GoodsTrainForecast> findByCorridorIdAndForecastDate(
            String corridorId,
            LocalDate forecastDate
    );
}