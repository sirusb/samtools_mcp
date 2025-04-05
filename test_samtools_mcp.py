#!/usr/bin/env python3
"""
Test file for Samtools MCP Server.
This file tests the functionality of the samtools_mcp module.
"""
import os
import unittest
import tempfile
import samtools_mcp

class TestSamtoolsMCP(unittest.TestCase):
    """Test cases for Samtools MCP."""

    def setUp(self):
        """Set up test environment."""
        self.test_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "bam")
        self.test1_bam = os.path.join(self.test_dir, "test1.bam")
        self.test2_bam = os.path.join(self.test_dir, "test2.bam")
        
        # Make sure the test files exist
        self.assertTrue(os.path.exists(self.test1_bam), f"Test file {self.test1_bam} does not exist")
        self.assertTrue(os.path.exists(self.test2_bam), f"Test file {self.test2_bam} does not exist")

    def test_view_count(self):
        """Test samtools view with count option."""
        # Test the view count for test1.bam
        result = samtools_mcp.samtools_view(self.test1_bam, count_only=True)
        self.assertEqual(result.strip(), "15", f"Expected 15 reads in {self.test1_bam}, got {result}")
        
        # Test the view count for test2.bam
        result = samtools_mcp.samtools_view(self.test2_bam, count_only=True)
        self.assertEqual(result.strip(), "12", f"Expected 12 reads in {self.test2_bam}, got {result}")

    def test_flagstat(self):
        """Test samtools flagstat."""
        # Test flagstat on test1.bam
        result = samtools_mcp.samtools_flagstat(self.test1_bam)
        self.assertIn("15 + 0 in total", result, "Expected 15 reads in flagstat output")
        self.assertIn("4 + 0 paired in sequencing", result, "Expected 4 paired reads in flagstat output")
        
        # Test flagstat on test2.bam
        result = samtools_mcp.samtools_flagstat(self.test2_bam)
        self.assertIn("12 + 0 in total", result, "Expected 12 reads in flagstat output")
        self.assertIn("2 + 0 paired in sequencing", result, "Expected 2 paired reads in flagstat output")

    def test_header_view(self):
        """Test viewing the header of a BAM file."""
        result = samtools_mcp.samtools_view(self.test1_bam, header_only=True)
        self.assertIn("@HD", result, "Expected @HD in header")
        self.assertIn("@SQ", result, "Expected @SQ in header")

    def test_view_with_flags(self):
        """Test view with flag filtering."""
        # Get only paired reads (flag 0x1)
        result = samtools_mcp.samtools_view(self.test1_bam, flags_required="1")
        lines = [line for line in result.split('\n') if line.strip()]
        self.assertEqual(len(lines), 4, f"Expected 4 paired reads, got {len(lines)}")

    def test_sort_and_index(self):
        """Test sorting and indexing a BAM file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            sorted_bam = os.path.join(tmpdir, "test1.sorted.bam")
            
            # Sort the BAM file
            sort_result = samtools_mcp.samtools_sort(self.test1_bam, output_file=sorted_bam)
            self.assertTrue(os.path.exists(sorted_bam), f"Sorted BAM file {sorted_bam} was not created")
            
            # Index the sorted BAM file
            index_result = samtools_mcp.samtools_index(sorted_bam)
            self.assertTrue(os.path.exists(sorted_bam + ".bai"), "BAM index file was not created")

    def test_version(self):
        """Test getting samtools version."""
        version = samtools_mcp.get_samtools_version()
        self.assertIn("samtools", version.lower(), "Expected 'samtools' in version string")
        self.assertIn("htslib", version.lower(), "Expected 'htslib' in version string")

    def test_help(self):
        """Test getting help information."""
        help_text = samtools_mcp.get_samtools_help()
        self.assertIn("usage", help_text.lower(), "Expected 'usage' in help text")
        
        # Test command-specific help
        view_help = samtools_mcp.get_command_help("view")
        self.assertIn("view", view_help.lower(), "Expected 'view' in view help text")

    def test_list_files(self):
        """Test listing BAM files."""
        result = samtools_mcp.samtools_list_files(self.test_dir)
        self.assertIn("test1.bam", result, "Expected test1.bam in file listing")
        self.assertIn("test2.bam", result, "Expected test2.bam in file listing")

if __name__ == "__main__":
    unittest.main()