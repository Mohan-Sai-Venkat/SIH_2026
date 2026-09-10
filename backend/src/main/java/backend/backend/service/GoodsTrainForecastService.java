package backend.backend.service;

import backend.backend.model.GoodsTrainForecast;
import backend.backend.repository.GoodsTrainForecastRepository;
import org.springframework.stereotype.Service;

import java.time.LocalDate;
import java.time.LocalTime;
import java.util.List;

@Service
public class GoodsTrainForecastService {

    private final GoodsTrainForecastRepository repository;

    public GoodsTrainForecastService(
            GoodsTrainForecastRepository repository) {
        this.repository = repository;
    }

    // =========================================================
    // GET ALL
    // =========================================================

    public List<GoodsTrainForecast> getAll() {
        return repository.findAll();
    }

    // =========================================================
    // GET BY ID
    // =========================================================

    public GoodsTrainForecast getById(Long id) {

        return repository.findById(id)
                .orElseThrow(() ->
                        new IllegalArgumentException(
                                "Goods train forecast not found: " + id
                        )
                );
    }

    // =========================================================
    // GET BY CORRIDOR AND DATE
    // =========================================================

    public List<GoodsTrainForecast> getByCorridorAndDate(
            String corridorId,
            LocalDate date) {

        return repository.findByCorridorIdAndForecastDate(
                corridorId,
                date
        );
    }

    // =========================================================
    // CREATE FORECAST
    // =========================================================

    public GoodsTrainForecast createForecast(
            GoodsTrainForecast forecast) {

        validateForecast(forecast);

        /*
         * Same corridor + same date:
         * update existing forecast instead of creating duplicate.
         */
        List<GoodsTrainForecast> existing =
                repository.findByCorridorIdAndForecastDate(
                        forecast.getCorridorId(),
                        forecast.getForecastDate()
                );

        if (!existing.isEmpty()) {

            GoodsTrainForecast current =
                    existing.get(0);

            current.setExpectedTrainCount(
                    forecast.getExpectedTrainCount()
            );

            current.setPeakStart(
                    forecast.getPeakStart()
            );

            current.setPeakEnd(
                    forecast.getPeakEnd()
            );

            current.setConfidence(
                    forecast.getConfidence()
            );

            return repository.save(current);
        }

        return repository.save(forecast);
    }

    // =========================================================
    // SAVE
    // =========================================================

    public GoodsTrainForecast save(
            GoodsTrainForecast forecast) {

        return createForecast(forecast);
    }

    // =========================================================
    // UPDATE FORECAST
    // =========================================================

    public GoodsTrainForecast updateForecast(
            Long id,
            GoodsTrainForecast forecast) {

        GoodsTrainForecast existing =
                getById(id);

        if (forecast.getCorridorId() != null
                && !forecast.getCorridorId().isBlank()) {

            existing.setCorridorId(
                    forecast.getCorridorId()
            );
        }

        if (forecast.getForecastDate() != null) {

            existing.setForecastDate(
                    forecast.getForecastDate()
            );
        }

        if (forecast.getExpectedTrainCount() != null
                && forecast.getExpectedTrainCount() >= 0) {

            existing.setExpectedTrainCount(
                    forecast.getExpectedTrainCount()
            );
        }

        existing.setPeakStart(
                forecast.getPeakStart()
        );

        existing.setPeakEnd(
                forecast.getPeakEnd()
        );

        if (forecast.getConfidence() != null) {

            existing.setConfidence(
                    forecast.getConfidence()
            );
        }

        validateForecast(existing);

        return repository.save(existing);
    }

    // =========================================================
    // UPDATE COMPATIBILITY
    // =========================================================

    public GoodsTrainForecast update(
            Long id,
            GoodsTrainForecast forecast) {

        return updateForecast(id, forecast);
    }

    // =========================================================
    // DELETE FORECAST
    // =========================================================

    public void deleteForecast(Long id) {

        if (!repository.existsById(id)) {

            throw new IllegalArgumentException(
                    "Goods train forecast not found: " + id
            );
        }

        repository.deleteById(id);
    }

    // =========================================================
    // DELETE COMPATIBILITY
    // =========================================================

    public void delete(Long id) {
        deleteForecast(id);
    }

    // =========================================================
    // EXPECTED TRAIN COUNT
    // =========================================================

    public int getExpectedTrainCount(
            String corridorId,
            LocalDate date) {

        return repository
                .findByCorridorIdAndForecastDate(
                        corridorId,
                        date
                )
                .stream()
                .mapToInt(forecast ->
                        forecast.getExpectedTrainCount() == null
                                ? 0
                                : forecast.getExpectedTrainCount()
                )
                .max()
                .orElse(0);
    }

    // =========================================================
    // OVERLAPPING GOODS TRAINS
    // =========================================================

    public int getOverlappingGoodsTrainCount(
            String corridorId,
            LocalDate date,
            LocalTime start,
            LocalTime end) {

        return repository
                .findByCorridorIdAndForecastDate(
                        corridorId,
                        date
                )
                .stream()
                .filter(forecast ->
                        overlaps(
                                start,
                                end,
                                forecast.getPeakStart(),
                                forecast.getPeakEnd()
                        )
                )
                .mapToInt(forecast ->
                        forecast.getExpectedTrainCount() == null
                                ? 0
                                : forecast.getExpectedTrainCount()
                )
                .max()
                .orElse(0);
    }

    // =========================================================
    // VALIDATION
    // =========================================================

    private void validateForecast(
            GoodsTrainForecast forecast) {

        if (forecast == null) {
            throw new IllegalArgumentException(
                    "Forecast data is required."
            );
        }

        if (forecast.getCorridorId() == null
                || forecast.getCorridorId().isBlank()) {

            throw new IllegalArgumentException(
                    "Corridor ID is required."
            );
        }

        if (forecast.getForecastDate() == null) {

            throw new IllegalArgumentException(
                    "Forecast date is required."
            );
        }

        if (forecast.getExpectedTrainCount() == null
                || forecast.getExpectedTrainCount() < 0) {

            throw new IllegalArgumentException(
                    "Expected train count cannot be negative."
            );
        }

        if (forecast.getConfidence() != null
                && (forecast.getConfidence() < 0
                || forecast.getConfidence() > 1)) {

            throw new IllegalArgumentException(
                    "Confidence must be between 0 and 1."
            );
        }
    }

    // =========================================================
    // TIME OVERLAP
    // =========================================================

    private boolean overlaps(
            LocalTime start1,
            LocalTime end1,
            LocalTime start2,
            LocalTime end2) {

        if (start1 == null
                || end1 == null
                || start2 == null
                || end2 == null) {

            return false;
        }

        return start1.isBefore(end2)
                && end1.isAfter(start2);
    }
}