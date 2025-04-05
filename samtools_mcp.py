# This is an MCP to interact with samtools
import subprocess
import os
import json
from typing import List, Dict, Optional, Any
from mcp.server.fastmcp import FastMCP


mcp = FastMCP("Samtools MCP")


def run_samtools_command(cmd_args: List[str]) -> str:
    """Run a samtools command and return its output."""
    try:
        # Check if we have any redirection symbols that require shell=True
        use_shell = False
        file_output = None
        output_redirect_index = -1
        
        # Look for output redirection in the command
        for i, arg in enumerate(cmd_args):
            if arg == ">":
                if i < len(cmd_args) - 1:
                    file_output = cmd_args[i + 1]
                    output_redirect_index = i
                    break
        
        # If we have redirection, remove those arguments and handle output redirection manually
        if output_redirect_index >= 0:
            cmd_args = cmd_args[:output_redirect_index]
        
        # Execute the command
        result = subprocess.run(["samtools"] + cmd_args, 
                              capture_output=True, 
                              text=True, 
                              check=False)
        
        # Handle errors
        if result.returncode != 0 and result.stderr:
            return f"Error: {result.stderr}"
        
        # Handle output redirection if needed
        if file_output:
            try:
                with open(file_output, 'w') as f:
                    f.write(result.stdout)
                return f"Output written to {file_output}"
            except Exception as e:
                return f"Error writing to {file_output}: {str(e)}"
        
        return result.stdout or result.stderr or "Command completed successfully with no output."
    except Exception as e:
        return f"Failed to execute samtools: {str(e)}"


@mcp.resource("help://samtools")
def get_samtools_help() -> str:
    """Get the general samtools help information."""
    return run_samtools_command(["--help"])


@mcp.resource("help://samtools/{command}")
def get_command_help(command: str) -> str:
    """Get help for a specific samtools command."""
    return run_samtools_command([command, "--help"])


@mcp.resource("version://samtools")
def get_samtools_version() -> str:
    """Get the samtools version information."""
    return run_samtools_command(["--version"])


@mcp.tool()
def samtools_view(
    input_file: str,
    output_format: Optional[str] = None,
    region: Optional[str] = None,
    header_only: Optional[bool] = False,
    count_only: Optional[bool] = False,
    flags_required: Optional[str] = None,
    flags_filter_out: Optional[str] = None,
    output_file: Optional[str] = None,
    additional_args: Optional[str] = None,
) -> str:
    """
    View and convert SAM/BAM/CRAM files.
    
    Args:
        input_file: Input SAM/BAM/CRAM file
        output_format: Output format (SAM, BAM, CRAM)
        region: Genomic region to view (format: chr:start-end)
        header_only: Only output the header section
        count_only: Only count records, don't output
        flags_required: Required flags (numeric value)
        flags_filter_out: Flags to filter out (numeric value)
        output_file: Output file name
        additional_args: Additional arguments as a string
    """
    cmd = ["view"]
    
    if output_format:
        if output_format.upper() == "BAM":
            cmd.append("-b")
        elif output_format.upper() == "CRAM":
            cmd.append("-C")
        elif output_format.upper() == "SAM":
            cmd.append("-S")
    
    if header_only:
        cmd.append("-H")
    
    if count_only:
        cmd.append("-c")
    
    if flags_required:
        cmd.extend(["-f", flags_required])
    
    if flags_filter_out:
        cmd.extend(["-F", flags_filter_out])
    
    if additional_args:
        cmd.extend(additional_args.split())
    
    cmd.append(input_file)
    
    if region:
        cmd.append(region)
    
    if output_file:
        cmd.extend([">", output_file])
    
    return run_samtools_command(cmd)


@mcp.tool()
def samtools_sort(
    input_file: str,
    output_file: Optional[str] = None,
    sort_by_name: Optional[bool] = False,
    threads: Optional[int] = None,
    memory_per_thread: Optional[str] = None,
    additional_args: Optional[str] = None,
) -> str:
    """
    Sort SAM/BAM/CRAM files.
    
    Args:
        input_file: Input file to sort
        output_file: Output file name (default: replaces the input file suffix with .sorted.bam)
        sort_by_name: Sort by read name instead of coordinate
        threads: Number of threads to use
        memory_per_thread: Memory per thread (e.g. '768M')
        additional_args: Additional arguments as a string
    """
    cmd = ["sort"]
    
    if sort_by_name:
        cmd.append("-n")
    
    if threads:
        cmd.extend(["-@", str(threads)])
    
    if memory_per_thread:
        cmd.extend(["-m", memory_per_thread])
    
    if additional_args:
        cmd.extend(additional_args.split())
    
    cmd.append(input_file)
    
    if output_file:
        cmd.extend(["-o", output_file])
    
    return run_samtools_command(cmd)


@mcp.tool()
def samtools_index(
    input_file: str,
    output_file: Optional[str] = None,
    csi_format: Optional[bool] = False,
    additional_args: Optional[str] = None,
) -> str:
    """
    Index SAM/BAM/CRAM files.
    
    Args:
        input_file: Input BAM/CRAM file to index
        output_file: Output index file (default: input_file.bai)
        csi_format: Generate CSI index instead of BAI
        additional_args: Additional arguments as a string
    """
    cmd = ["index"]
    
    if csi_format:
        cmd.append("-c")
    
    if additional_args:
        cmd.extend(additional_args.split())
    
    cmd.append(input_file)
    
    if output_file:
        cmd.append(output_file)
    
    return run_samtools_command(cmd)


@mcp.tool()
def samtools_flagstat(
    input_file: str,
) -> str:
    """
    Generate statistics on a BAM/CRAM file.
    
    Args:
        input_file: Input BAM/CRAM file
    """
    cmd = ["flagstat", input_file]
    return run_samtools_command(cmd)


@mcp.tool()
def samtools_idxstats(
    input_file: str,
) -> str:
    """
    Generate statistics from a BAM/CRAM index.
    
    Args:
        input_file: Indexed BAM/CRAM file
    """
    cmd = ["idxstats", input_file]
    return run_samtools_command(cmd)


@mcp.tool()
def samtools_faidx(
    input_file: str,
    regions: Optional[List[str]] = None,
    output_file: Optional[str] = None,
) -> str:
    """
    Index FASTA files or extract sequences from indexed FASTA.
    
    Args:
        input_file: Input FASTA file
        regions: List of regions to extract (e.g. ['chr1', 'chr2:1-1000'])
        output_file: Output file name for extracted sequences
    """
    cmd = ["faidx", input_file]
    
    if regions:
        cmd.extend(regions)
    
    if output_file:
        cmd.extend([">", output_file])
    
    return run_samtools_command(cmd)


@mcp.tool()
def samtools_merge(
    output_file: str,
    input_files: List[str],
    threads: Optional[int] = None,
    additional_args: Optional[str] = None,
) -> str:
    """
    Merge multiple sorted BAM/CRAM files.
    
    Args:
        output_file: Output merged file name
        input_files: List of input BAM/CRAM files to merge
        threads: Number of threads to use
        additional_args: Additional arguments as a string
    """
    cmd = ["merge"]
    
    if threads:
        cmd.extend(["-@", str(threads)])
    
    if additional_args:
        cmd.extend(additional_args.split())
    
    cmd.append(output_file)
    cmd.extend(input_files)
    
    return run_samtools_command(cmd)


@mcp.tool()
def samtools_depth(
    input_files: List[str],
    region: Optional[str] = None,
    output_file: Optional[str] = None,
    additional_args: Optional[str] = None,
) -> str:
    """
    Calculate the depth at each position in a BAM/CRAM file.
    
    Args:
        input_files: List of input BAM/CRAM files
        region: Only calculate depth in this region (format: chr:start-end)
        output_file: Output file name
        additional_args: Additional arguments as a string
    """
    cmd = ["depth"]
    
    if additional_args:
        cmd.extend(additional_args.split())
    
    cmd.extend(input_files)
    
    if region:
        cmd.append(region)
    
    if output_file:
        cmd.extend([">", output_file])
    
    return run_samtools_command(cmd)


@mcp.tool()
def samtools_list_files(directory: str = ".") -> str:
    """
    List BAM/SAM/CRAM files in a directory.
    
    Args:
        directory: Directory to search for files
    """
    try:
        files = []
        for file in os.listdir(directory):
            if file.endswith(('.bam', '.sam', '.cram')):
                files.append(file)
        
        if not files:
            return f"No BAM/SAM/CRAM files found in {directory}"
        
        return "\n".join(files)
    except Exception as e:
        return f"Error listing files: {str(e)}"


@mcp.prompt()
def show_sam_file_prompt(file_path: str) -> str:
    """
    Prompt to view a SAM/BAM/CRAM file with headers.
    
    Args:
        file_path: Path to the SAM/BAM/CRAM file to view
    """
    return f"""
    View the contents of file {file_path} with headers:
    
    Use the samtools_view tool with the following parameters:
    - input_file: {file_path}
    - header_only: false
    """


@mcp.prompt()
def get_file_statistics_prompt(file_path: str) -> str:
    """
    Prompt to get statistics for a BAM/CRAM file.
    
    Args:
        file_path: Path to the BAM/CRAM file to analyze
    """
    return f"""
    Get statistics for file {file_path}:
    
    First, check if the file is indexed:
    ```
    samtools_index(input_file="{file_path}")
    ```
    
    Then get the statistics:
    ```
    samtools_flagstat(input_file="{file_path}")
    samtools_idxstats(input_file="{file_path}")
    ```
    """


@mcp.prompt()
def index_and_sort_workflow_prompt(file_path: str) -> str:
    """
    Prompt for a common workflow: sort a BAM file and index it.
    
    Args:
        file_path: Path to the BAM file to sort and index
    """
    output_file = file_path.replace(".bam", ".sorted.bam")
    if output_file == file_path:
        output_file = file_path + ".sorted"
        
    return f"""
    Sort and index {file_path}:
    
    1. Sort the file:
    ```
    samtools_sort(input_file="{file_path}", output_file="{output_file}")
    ```
    
    2. Index the sorted file:
    ```
    samtools_index(input_file="{output_file}")
    ```
    """


if __name__ == "__main__":
    mcp.run()










