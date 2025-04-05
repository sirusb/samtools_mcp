# Samtools MCP

This is a Model Context Protocol (MCP) server for interacting with samtools, a suite of programs for working with high-throughput sequencing data.

## Installation

1. Make sure you have samtools installed and available in your PATH:
   ```
   which samtools
   ```

2. Install the MCP Python SDK:
   ```
   pip install mcp
   ```

## Usage

Run the server:

```
python samtools_mcp.py
```

Or use the MCP CLI:

```
mcp run samtools_mcp.py
```

## Available Tools

The MCP server provides the following tools:

- `samtools_view`: View and convert SAM/BAM/CRAM files
- `samtools_sort`: Sort SAM/BAM/CRAM files
- `samtools_index`: Index SAM/BAM/CRAM files
- `samtools_flagstat`: Generate statistics on BAM/CRAM files
- `samtools_idxstats`: Generate statistics from a BAM/CRAM index
- `samtools_faidx`: Index FASTA files or extract sequences
- `samtools_merge`: Merge multiple sorted BAM/CRAM files
- `samtools_depth`: Calculate depth at each position
- `samtools_list_files`: List BAM/SAM/CRAM files in a directory

## Available Resources

- `help://samtools`: General samtools help information
- `help://samtools/{command}`: Help for a specific samtools command
- `version://samtools`: Samtools version information

## Available Prompts

- `show_sam_file_prompt`: View a SAM/BAM/CRAM file with headers
- `get_file_statistics_prompt`: Get statistics for a BAM/CRAM file
- `index_and_sort_workflow_prompt`: Sort a BAM file and index it

## Example Usage

Using the MCP with Claude:

```
I have a BAM file called "sample.bam". Can you help me sort and index it?
```

Claude can then use the `index_and_sort_workflow_prompt` to guide you through the process.

## License

MIT