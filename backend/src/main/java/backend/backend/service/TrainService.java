package backend.backend.service;

import backend.backend.model.Train;
import backend.backend.repository.TrainRepository;
import org.springframework.stereotype.Service;

import java.time.LocalTime;
import java.util.List;

@Service
public class TrainService {

    private final TrainRepository repository;

    public TrainService(TrainRepository repository) {
        this.repository = repository;
    }

    // Get all trains
    public List<Train> getAll() {
        return repository.findAll();
    }

    // Get trains by corridor
    public List<Train> getByCorridor(String corridorId) {
        return repository.findByCorridorId(corridorId);
    }

    // Add a new train timetable
    public Train createTrain(Train train) {

        if (train.getTrainId() == null ||
                train.getTrainId().isBlank()) {

            throw new IllegalArgumentException(
                    "Train ID is required."
            );
        }

        if (train.getCorridorId() == null ||
                train.getCorridorId().isBlank()) {

            throw new IllegalArgumentException(
                    "Corridor ID is required."
            );
        }

        if (train.getArrivalTime() == null ||
                train.getDepartureTime() == null) {

            throw new IllegalArgumentException(
                    "Arrival time and departure time are required."
            );
        }

        if (!train.getArrivalTime()
                .isBefore(train.getDepartureTime())) {

            throw new IllegalArgumentException(
                    "Arrival time must be before departure time."
            );
        }

        if (train.getTrainType() == null ||
                train.getTrainType().isBlank()) {

            train.setTrainType("PASSENGER");
        }

        if (train.getPriority() == null ||
                train.getPriority().isBlank()) {

            train.setPriority("NORMAL");
        }

        return repository.save(train);
    }

    // Update an existing train timetable
    public Train updateTrain(String trainId, Train updatedTrain) {

        Train existing = repository.findAll()
                .stream()
                .filter(train ->
                        train.getTrainId() != null &&
                                train.getTrainId().equalsIgnoreCase(trainId))
                .findFirst()
                .orElseThrow(() ->
                        new IllegalArgumentException(
                                "Train not found: " + trainId
                        ));

        if (updatedTrain.getTrainName() != null &&
                !updatedTrain.getTrainName().isBlank()) {

            existing.setTrainName(
                    updatedTrain.getTrainName()
            );
        }

        if (updatedTrain.getCorridorId() != null &&
                !updatedTrain.getCorridorId().isBlank()) {

            existing.setCorridorId(
                    updatedTrain.getCorridorId()
            );
        }

        if (updatedTrain.getArrivalTime() != null) {

            existing.setArrivalTime(
                    updatedTrain.getArrivalTime()
            );
        }

        if (updatedTrain.getDepartureTime() != null) {

            existing.setDepartureTime(
                    updatedTrain.getDepartureTime()
            );
        }

        if (updatedTrain.getTrainType() != null &&
                !updatedTrain.getTrainType().isBlank()) {

            existing.setTrainType(
                    updatedTrain.getTrainType()
            );
        }

        if (updatedTrain.getPriority() != null &&
                !updatedTrain.getPriority().isBlank()) {

            existing.setPriority(
                    updatedTrain.getPriority()
            );
        }

        if (!existing.getArrivalTime()
                .isBefore(existing.getDepartureTime())) {

            throw new IllegalArgumentException(
                    "Arrival time must be before departure time."
            );
        }

        return repository.save(existing);
    }

    // Delete a train timetable
    public void deleteTrain(String trainId) {

        Train existing = repository.findAll()
                .stream()
                .filter(train ->
                        train.getTrainId() != null &&
                                train.getTrainId().equalsIgnoreCase(trainId))
                .findFirst()
                .orElseThrow(() ->
                        new IllegalArgumentException(
                                "Train not found: " + trainId
                        ));

        repository.delete(existing);
    }

    // Find trains conflicting with a maintenance block
    public List<Train> getConflictingTrains(
            String corridorId,
            LocalTime start,
            LocalTime end) {

        return repository
                .findByCorridorId(corridorId)
                .stream()
                .filter(train ->
                        train.getArrivalTime() != null &&
                                train.getDepartureTime() != null)
                .filter(train ->
                        overlaps(
                                start,
                                end,
                                train.getArrivalTime(),
                                train.getDepartureTime()
                        ))
                .toList();
    }

    // Find high/critical priority trains
    public List<Train> getHighPriorityTrains(
            String corridorId) {

        return repository
                .findByCorridorId(corridorId)
                .stream()
                .filter(train ->
                        train.getPriority() != null &&
                                (
                                        train.getPriority()
                                                .equalsIgnoreCase("Critical")
                                                ||
                                                train.getPriority()
                                                        .equalsIgnoreCase("High")
                                ))
                .toList();
    }

    private boolean overlaps(
            LocalTime start1,
            LocalTime end1,
            LocalTime start2,
            LocalTime end2) {

        if (start1 == null ||
                end1 == null ||
                start2 == null ||
                end2 == null) {

            return false;
        }

        return start1.isBefore(end2)
                && end1.isAfter(start2);
    }
}