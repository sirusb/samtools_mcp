# SAMtools MCP (Model Control Protocol)

A Model Control Protocol implementation for SAMtools, providing a standardized interface for working with SAM/BAM/CRAM files.

## Features

- View and convert SAM/BAM/CRAM files
- Sort alignment files
- Index BAM/CRAM files
- Generate statistics
- Merge multiple BAM files
- Calculate read depth
- Index FASTA files
- And more...

## Installation

### Using Docker (Recommended)

The easiest way to use SAMtools MCP is through Docker:

```bash
# Pull the Docker image
docker pull nadhir/samtools-mcp:latest

# Run the container
docker run -it --rm nadhir/samtools-mcp:latest

# To process BAM files, mount a volume:
docker run -it --rm -v /path/to/your/bam/files:/data nadhir/samtools-mcp:latest
```

### Local Installation

1. Clone the repository:
```bash
git clone https://github.com/your-username/samtools_mcp.git
cd samtools_mcp
```

2. Install dependencies:
```bash
pip install uv
uv pip install -r requirements.txt
```

## Configuration

### MCP Server Configuration

To configure the MCP server to use the Docker image, add the following to your MCP configuration file:

```json
{
  "servers": {
    "samtools": {
      "type": "docker",
      "image": "nadhir/samtools-mcp:latest",
      "volumes": [
        {
          "source": "/path/to/your/data",
          "target": "/data"
        }
      ]
    }
  }
}
```

### Local MCP Configuration

To configure the MCP to run using `uv`, add the following to your `~/.cursor/mcp.json`:

```json
{
  "samtools_mcp": {
    "command": "uv",
    "args": ["run", "--with", "fastmcp", "fastmcp", "run", "/path/to/samtools_mcp.py"]
  }
}
```

Replace `/path/to/samtools_mcp.py` with the actual path to your `samtools_mcp.py` file.

## Usage

### Basic Commands

1. View BAM file:
```python
from samtools_mcp import SamtoolsMCP

mcp = SamtoolsMCP()
result = mcp.view(input_file="/data/example.bam")
```

2. Sort BAM file:
```python
result = mcp.sort(input_file="/data/example.bam", output_file="/data/sorted.bam")
```

3. Index BAM file:
```python
result = mcp.index(input_file="/data/sorted.bam")
```

### Advanced Usage

1. View specific region with flags:
```python
result = mcp.view(
    input_file="/data/example.bam",
    region="chr1:1000-2000",
    flags_required="0x2",
    output_format="SAM"
)
```

2. Sort by read name:
```python
result = mcp.sort(
    input_file="/data/example.bam",
    output_file="/data/namesorted.bam",
    sort_by_name=True
)
```

3. Calculate depth with multiple input files:
```python
result = mcp.depth(
    input_files=["/data/sample1.bam", "/data/sample2.bam"],
    region="chr1:1-1000000"
)
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.