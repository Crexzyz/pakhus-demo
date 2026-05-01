import time
import torch
import torch.nn as nn
import torch.optim as optim


def check_cuda():
    """Check CUDA availability and print device info."""
    print("=" * 60)
    print("CUDA Environment Check")
    print("=" * 60)
    print(f"PyTorch version:       {torch.__version__}")
    print(f"CUDA available:        {torch.cuda.is_available()}")
    print(f"CUDA version (runtime):{torch.version.cuda}")

    if torch.cuda.is_available():
        print(f"GPU device count:      {torch.cuda.device_count()}")
        print(f"Current device:        {torch.cuda.current_device()}")
        print(f"Device name:           {torch.cuda.get_device_name(0)}")
        print(f"Device capability:     {torch.cuda.get_device_capability(0)}")
    else:
        print("\n[WARNING] CUDA is NOT available. Running on CPU only.")
        print("Ensure you have CUDA 11.4 drivers installed and a compatible GPU.")

    print("=" * 60)
    return torch.cuda.is_available()


def benchmark_matmul(size=4096, iterations=10):
    """Benchmark matrix multiplication on CPU vs GPU."""
    print(f"\n{'='*60}")
    print(f"Benchmark: Matrix Multiplication ({size}x{size}, {iterations} iters)")
    print(f"{'='*60}")

    # CPU benchmark
    a_cpu = torch.randn(size, size)
    b_cpu = torch.randn(size, size)

    start = time.perf_counter()
    for _ in range(iterations):
        _ = torch.mm(a_cpu, b_cpu)
    cpu_time = time.perf_counter() - start
    print(f"CPU time: {cpu_time:.4f} seconds")

    # GPU benchmark
    if torch.cuda.is_available():
        a_gpu = a_cpu.cuda()
        b_gpu = b_cpu.cuda()

        # Warm-up
        for _ in range(3):
            _ = torch.mm(a_gpu, b_gpu)
        torch.cuda.synchronize()

        start = time.perf_counter()
        for _ in range(iterations):
            _ = torch.mm(a_gpu, b_gpu)
        torch.cuda.synchronize()
        gpu_time = time.perf_counter() - start

        print(f"GPU time: {gpu_time:.4f} seconds")
        print(f"Speedup:  {cpu_time / gpu_time:.2f}x")
    else:
        print("GPU benchmark skipped (CUDA not available)")


class SimpleNet(nn.Module):
    """A simple feedforward network for benchmarking."""

    def __init__(self, input_size=1024, hidden_size=2048, output_size=10):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(input_size, hidden_size),
            nn.ReLU(),
            nn.Linear(hidden_size, hidden_size),
            nn.ReLU(),
            nn.Linear(hidden_size, output_size),
        )

    def forward(self, x):
        return self.net(x)


def benchmark_training(epochs=20, batch_size=256, input_size=1024):
    """Benchmark neural network training on CPU vs GPU."""
    print(f"\n{'='*60}")
    print(f"Benchmark: Neural Network Training ({epochs} epochs, batch={batch_size})")
    print(f"{'='*60}")

    # Generate synthetic data
    data = torch.randn(batch_size * 10, input_size)
    labels = torch.randint(0, 10, (batch_size * 10,))

    def train_on_device(device_name):
        device = torch.device(device_name)
        model = SimpleNet(input_size=input_size).to(device)
        criterion = nn.CrossEntropyLoss()
        optimizer = optim.Adam(model.parameters(), lr=0.001)

        local_data = data.to(device)
        local_labels = labels.to(device)

        if device_name == "cuda":
            torch.cuda.synchronize()

        start = time.perf_counter()
        for epoch in range(epochs):
            for i in range(0, len(local_data), batch_size):
                batch_x = local_data[i:i + batch_size]
                batch_y = local_labels[i:i + batch_size]

                optimizer.zero_grad()
                outputs = model(batch_x)
                loss = criterion(outputs, batch_y)
                loss.backward()
                optimizer.step()

        if device_name == "cuda":
            torch.cuda.synchronize()

        elapsed = time.perf_counter() - start
        print(f"  {device_name.upper()} time: {elapsed:.4f} seconds (final loss: {loss.item():.4f})")
        return elapsed

    cpu_time = train_on_device("cpu")

    if torch.cuda.is_available():
        gpu_time = train_on_device("cuda")
        print(f"  Speedup:  {cpu_time / gpu_time:.2f}x")
    else:
        print("  GPU training skipped (CUDA not available)")


if __name__ == "__main__":
    has_cuda = check_cuda()
    benchmark_matmul()
    benchmark_training()

    print(f"\n{'='*60}")
    if has_cuda:
        print("Demo complete. GPU acceleration is available and working!")
    else:
        print("Demo complete. Only CPU benchmarks were run.")
        print("To use GPU acceleration, ensure CUDA 11.4 toolkit and")
        print("compatible NVIDIA drivers are installed.")
    print(f"{'='*60}")
