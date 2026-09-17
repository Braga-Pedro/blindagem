package io.github.bragapedro.blindagem;

import org.springframework.boot.SpringApplication;

public class TestBlindagemApplication {

	public static void main(String[] args) {
		SpringApplication.from(BlindagemApplication::main).with(TestcontainersConfiguration.class).run(args);
	}

}
