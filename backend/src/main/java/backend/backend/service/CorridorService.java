package backend.backend.service;

import backend.backend.exception.ResourceNotFoundException;
import backend.backend.model.Corridor;
import backend.backend.repository.CorridorRepository;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class CorridorService {

    private final CorridorRepository repository;

    public CorridorService(CorridorRepository repository) {
        this.repository = repository;
    }

    public List<Corridor> getAll() {
        return repository.findAll();
    }

    public Corridor getByCorridorId(String corridorId) {

        return repository.findByCorridorId(corridorId)
                .orElseThrow(() ->
                        new ResourceNotFoundException(
                                "Corridor not found: " + corridorId
                        ));
    }

    public boolean isAvailable(String corridorId) {

        Corridor corridor = getByCorridorId(corridorId);

        return corridor.getStatus() != null
                && corridor.getStatus().equalsIgnoreCase("AVAILABLE")
                && corridor.getAvailabilityPercent() != null
                && corridor.getAvailabilityPercent() > 0;
    }
}