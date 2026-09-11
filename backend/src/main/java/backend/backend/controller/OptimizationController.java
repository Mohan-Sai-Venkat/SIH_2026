package backend.backend.controller;

import backend.backend.service.RailwayOptimizationClient;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/optimization")
public class OptimizationController {

    private final RailwayOptimizationClient optimizationClient;

    public OptimizationController(
            RailwayOptimizationClient optimizationClient) {
        this.optimizationClient = optimizationClient;
    }

    @PostMapping(
            value = "/run",
            produces = MediaType.APPLICATION_JSON_VALUE
    )
    public ResponseEntity<String> runOptimization() {

        return ResponseEntity.ok(
                optimizationClient.runOptimization()
        );
    }
}