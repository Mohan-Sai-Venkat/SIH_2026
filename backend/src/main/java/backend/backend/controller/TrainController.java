package backend.backend.controller;

import backend.backend.model.Train;
import backend.backend.service.TrainService;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.*;

import java.time.LocalTime;
import java.util.List;

@RestController
@RequestMapping("/api/trains")
public class TrainController {

    private final TrainService service;

    public TrainController(TrainService service) {
        this.service = service;
    }

    // Get all trains
    @GetMapping
    public List<Train> getAllTrains() {
        return service.getAll();
    }

    // Get trains by corridor
    @GetMapping("/corridor/{corridorId}")
    public List<Train> getByCorridor(
            @PathVariable String corridorId) {

        return service.getByCorridor(corridorId);
    }

    // Add new train timetable
    @PostMapping
    @ResponseStatus(HttpStatus.CREATED)
    public Train createTrain(
            @RequestBody Train train) {

        return service.createTrain(train);
    }

    // Update train timetable
    @PutMapping("/{trainId}")
    public Train updateTrain(
            @PathVariable String trainId,
            @RequestBody Train train) {

        return service.updateTrain(
                trainId,
                train
        );
    }

    // Delete train timetable
    @DeleteMapping("/{trainId}")
    @ResponseStatus(HttpStatus.NO_CONTENT)
    public void deleteTrain(
            @PathVariable String trainId) {

        service.deleteTrain(trainId);
    }

    // Get trains conflicting with a block
    @GetMapping("/conflicts")
    public List<Train> getConflictingTrains(
            @RequestParam String corridorId,
            @RequestParam String start,
            @RequestParam String end) {

        return service.getConflictingTrains(
                corridorId,
                LocalTime.parse(start),
                LocalTime.parse(end)
        );
    }

    // Get high/critical priority trains
    @GetMapping("/high-priority/{corridorId}")
    public List<Train> getHighPriorityTrains(
            @PathVariable String corridorId) {

        return service.getHighPriorityTrains(
                corridorId
        );
    }
}