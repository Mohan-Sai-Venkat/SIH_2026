package backend.backend.controller;

import backend.backend.model.Corridor;
import backend.backend.service.CorridorService;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/corridors")
public class CorridorController {

    private final CorridorService service;

    public CorridorController(CorridorService service) {
        this.service = service;
    }

    @GetMapping
    public List<Corridor> getAll() {
        return service.getAll();
    }

    @GetMapping("/{corridorId}")
    public Corridor getByCorridorId(
            @PathVariable String corridorId) {

        return service.getByCorridorId(corridorId);
    }
}