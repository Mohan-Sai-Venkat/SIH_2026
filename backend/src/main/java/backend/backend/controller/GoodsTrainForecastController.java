package backend.backend.controller;

import backend.backend.model.GoodsTrainForecast;
import backend.backend.service.GoodsTrainForecastService;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.*;

import java.time.LocalDate;
import java.util.List;

@RestController
@RequestMapping("/api/goods-train-forecast")
public class GoodsTrainForecastController {

    private final GoodsTrainForecastService service;

    public GoodsTrainForecastController(
            GoodsTrainForecastService service) {
        this.service = service;
    }

    // Get all goods train forecasts
    @GetMapping
    public List<GoodsTrainForecast> getAllForecasts() {
        return service.getAll();
    }

    // Get forecast by corridor and date
    @GetMapping("/corridor/{corridorId}/date/{date}")
    public List<GoodsTrainForecast> getByCorridorAndDate(
            @PathVariable String corridorId,
            @PathVariable LocalDate date) {

        return service.getByCorridorAndDate(
                corridorId,
                date
        );
    }

    // Add a new goods train forecast
    @PostMapping
    @ResponseStatus(HttpStatus.CREATED)
    public GoodsTrainForecast createForecast(
            @RequestBody GoodsTrainForecast forecast) {

        return service.createForecast(forecast);
    }

    // Update forecast
    @PutMapping("/{id}")
    public GoodsTrainForecast updateForecast(
            @PathVariable Long id,
            @RequestBody GoodsTrainForecast forecast) {

        return service.updateForecast(
                id,
                forecast
        );
    }

    // Delete forecast
    @DeleteMapping("/{id}")
    @ResponseStatus(HttpStatus.NO_CONTENT)
    public void deleteForecast(
            @PathVariable Long id) {

        service.deleteForecast(id);
    }

    // Get total expected goods trains
    @GetMapping("/expected")
    public int getExpectedTrainCount(
            @RequestParam String corridorId,
            @RequestParam LocalDate date) {

        return service.getExpectedTrainCount(
                corridorId,
                date
        );
    }

    // Get overlapping goods trains for a proposed block
    @GetMapping("/overlap")
    public int getOverlappingGoodsTrainCount(
            @RequestParam String corridorId,
            @RequestParam LocalDate date,
            @RequestParam String start,
            @RequestParam String end) {

        return service.getOverlappingGoodsTrainCount(
                corridorId,
                date,
                java.time.LocalTime.parse(start),
                java.time.LocalTime.parse(end)
        );
    }
}