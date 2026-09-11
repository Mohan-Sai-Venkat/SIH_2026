package backend.backend.service;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.MediaType;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestClient;

@Service
public class RailwayOptimizationClient {

    private final RestClient restClient;

    public RailwayOptimizationClient(
            @Value("${optimization.api.url:https://railway-optimization.onrender.com}")
            String optimizationApiUrl) {

        this.restClient = RestClient.builder()
                .baseUrl(optimizationApiUrl)
                .build();
    }

    public String runOptimization() {

        return restClient.post()
                .uri("/api/optimize")
                .contentType(MediaType.APPLICATION_JSON)
                .retrieve()
                .body(String.class);
    }
}