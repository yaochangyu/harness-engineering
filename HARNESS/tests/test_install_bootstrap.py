#!/usr/bin/env python3
"""
Test suite for HARNESS bootstrap behavior.

Tests cover:
- parse_bootstrap_args: defaults, overrides, forwarding
- tarball_url: derivation from repo/branch/tag
- acquire_repo: file:// tarball path with git disabled
- idempotent reuse: repeated calls with same args
- invalid-target abort: error handling for bad targets
"""

import unittest
import tempfile
import shutil
from pathlib import Path
from unittest.mock import patch, MagicMock
import sys
import os

# Add HARNESS to path so we can import install module
harness_dir = Path(__file__).parent.parent.resolve()
sys.path.insert(0, str(harness_dir))

try:
    import install
except ImportError as e:
    # Expected to fail initially; test will catch AttributeError
    install = None


class TestParseBootstrapArgs(unittest.TestCase):
    """Test parse_bootstrap_args function."""

    def test_parse_bootstrap_args_exists(self):
        """Given: install module loaded, When: accessing parse_bootstrap_args, Then: function exists."""
        self.assertTrue(
            hasattr(install, 'parse_bootstrap_args'),
            "install module must have parse_bootstrap_args function"
        )

    def test_parse_bootstrap_args_default_values(self):
        """Given: no args provided, When: parse_bootstrap_args called, Then: returns defaults."""
        if not hasattr(install, 'parse_bootstrap_args'):
            self.skipTest("parse_bootstrap_args not implemented")
        
        result = install.parse_bootstrap_args([])
        
        self.assertEqual(result.get('repo'), install.DEFAULT_REPO_URL)
        self.assertEqual(result.get('branch'), 'main')
        self.assertIsNone(result.get('tag'))
        self.assertTrue(str(result.get('target')).endswith('harness-engineering'))
        self.assertTrue(result.get('git_enabled', True))

    def test_parse_bootstrap_args_override_repo(self):
        """Given: --repo=https://github.com/org/repo, When: parse_bootstrap_args called, Then: repo is set."""
        if not hasattr(install, 'parse_bootstrap_args'):
            self.skipTest("parse_bootstrap_args not implemented")
        
        result = install.parse_bootstrap_args(['--repo=https://github.com/org/repo'])
        
        self.assertEqual(result.get('repo'), 'https://github.com/org/repo')

    def test_parse_bootstrap_args_override_branch(self):
        """Given: --branch=develop, When: parse_bootstrap_args called, Then: branch is set."""
        if not hasattr(install, 'parse_bootstrap_args'):
            self.skipTest("parse_bootstrap_args not implemented")
        
        result = install.parse_bootstrap_args(['--branch=develop'])
        
        self.assertEqual(result.get('branch'), 'develop')

    def test_parse_bootstrap_args_override_tag(self):
        """Given: --tag=v1.0.0, When: parse_bootstrap_args called, Then: tag is set."""
        if not hasattr(install, 'parse_bootstrap_args'):
            self.skipTest("parse_bootstrap_args not implemented")
        
        result = install.parse_bootstrap_args(['--tag=v1.0.0'])
        
        self.assertEqual(result.get('tag'), 'v1.0.0')

    def test_parse_bootstrap_args_override_target(self):
        """Given: --target=/tmp/harness, When: parse_bootstrap_args called, Then: target is set."""
        if not hasattr(install, 'parse_bootstrap_args'):
            self.skipTest("parse_bootstrap_args not implemented")
        
        result = install.parse_bootstrap_args(['--target=/tmp/harness'])
        
        self.assertEqual(result.get('target'), '/tmp/harness')

    def test_parse_bootstrap_args_disable_git(self):
        """Given: --no-git, When: parse_bootstrap_args called, Then: git_enabled is False."""
        if not hasattr(install, 'parse_bootstrap_args'):
            self.skipTest("parse_bootstrap_args not implemented")
        
        result = install.parse_bootstrap_args(['--no-git'])
        
        self.assertFalse(result.get('git_enabled', True))

    def test_parse_bootstrap_args_multiple_overrides(self):
        """Given: multiple args, When: parse_bootstrap_args called, Then: all are applied."""
        if not hasattr(install, 'parse_bootstrap_args'):
            self.skipTest("parse_bootstrap_args not implemented")
        
        result = install.parse_bootstrap_args([
            '--repo=https://github.com/org/repo',
            '--branch=feature',
            '--target=/opt/harness',
            '--no-git'
        ])
        
        self.assertEqual(result.get('repo'), 'https://github.com/org/repo')
        self.assertEqual(result.get('branch'), 'feature')
        self.assertEqual(result.get('target'), '/opt/harness')
        self.assertFalse(result.get('git_enabled', True))


class TestTarballUrl(unittest.TestCase):
    """Test tarball_url derivation function."""

    def test_tarball_url_exists(self):
        """Given: install module loaded, When: accessing tarball_url, Then: function exists."""
        self.assertTrue(
            hasattr(install, 'tarball_url'),
            "install module must have tarball_url function"
        )

    def test_tarball_url_from_repo_and_branch(self):
        """Given: repo and branch, When: tarball_url called, Then: returns GitHub archive URL."""
        if not hasattr(install, 'tarball_url'):
            self.skipTest("tarball_url not implemented")
        
        url = install.tarball_url(
            repo='https://github.com/org/repo',
            branch='main'
        )
        
        # Expected format: https://github.com/org/repo/archive/refs/heads/main.tar.gz
        self.assertIn('github.com', url)
        self.assertIn('archive', url)
        self.assertIn('main', url)
        self.assertTrue(url.endswith('.tar.gz'))

    def test_tarball_url_from_repo_and_tag(self):
        """Given: repo and tag, When: tarball_url called, Then: returns GitHub archive URL with tag."""
        if not hasattr(install, 'tarball_url'):
            self.skipTest("tarball_url not implemented")
        
        url = install.tarball_url(
            repo='https://github.com/org/repo',
            tag='v1.0.0'
        )
        
        # Expected format: https://github.com/org/repo/archive/refs/tags/v1.0.0.tar.gz
        self.assertIn('github.com', url)
        self.assertIn('archive', url)
        self.assertIn('v1.0.0', url)
        self.assertTrue(url.endswith('.tar.gz'))

    def test_tarball_url_branch_takes_precedence_over_tag(self):
        """Given: both branch and tag, When: tarball_url called, Then: branch takes precedence."""
        if not hasattr(install, 'tarball_url'):
            self.skipTest("tarball_url not implemented")
        
        url = install.tarball_url(
            repo='https://github.com/org/repo',
            branch='develop',
            tag='v1.0.0'
        )
        
        # Branch should take precedence
        self.assertIn('develop', url)
        self.assertNotIn('v1.0.0', url)


class TestAcquireRepo(unittest.TestCase):
    """Test acquire_repo function for file:// tarball handling."""

    def setUp(self):
        """Create temporary directories for testing."""
        self.temp_dir = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.temp_dir, ignore_errors=True)

    def test_acquire_repo_exists(self):
        """Given: install module loaded, When: accessing acquire_repo, Then: function exists."""
        self.assertTrue(
            hasattr(install, 'acquire_repo'),
            "install module must have acquire_repo function"
        )

    def test_acquire_repo_file_url_with_git_disabled(self):
        """Given: file:// URL and git_enabled=False, When: acquire_repo called, Then: extracts tarball."""
        if not hasattr(install, 'acquire_repo'):
            self.skipTest("acquire_repo not implemented")
        
        # Create a minimal tarball for testing
        import tarfile
        tarball_path = Path(self.temp_dir) / "test.tar.gz"
        with tarfile.open(tarball_path, "w:gz") as tar:
            import io
            info = tarfile.TarInfo(name="test-repo/HARNESS/install.py")
            data = b"print('ok')"
            info.size = len(data)
            tar.addfile(info, io.BytesIO(data))
        
        target_dir = Path(self.temp_dir) / "target"
        target_dir.mkdir()
        
        file_url = f"file://{tarball_path}"
        result = install.acquire_repo(
            url=file_url,
            target=str(target_dir),
            git_enabled=False
        )
        
        # Should extract successfully
        self.assertTrue(result)
        # Target should contain extracted files
        self.assertTrue((target_dir / "HARNESS" / "install.py").exists())

    def test_acquire_repo_idempotent_reuse(self):
        """Given: same target already exists, When: acquire_repo called twice, Then: second call succeeds."""
        if not hasattr(install, 'acquire_repo'):
            self.skipTest("acquire_repo not implemented")
        
        import tarfile
        tarball_path = Path(self.temp_dir) / "test.tar.gz"
        with tarfile.open(tarball_path, "w:gz") as tar:
            import io
            info = tarfile.TarInfo(name="test-repo/HARNESS/install.py")
            data = b"print('ok')"
            info.size = len(data)
            tar.addfile(info, io.BytesIO(data))
        
        target_dir = Path(self.temp_dir) / "target"
        target_dir.mkdir()
        
        file_url = f"file://{tarball_path}"
        
        # First call
        result1 = install.acquire_repo(
            url=file_url,
            target=str(target_dir),
            git_enabled=False
        )
        self.assertTrue(result1)
        self.assertTrue((target_dir / "HARNESS" / "install.py").exists())
        
        # Second call with same target (idempotent)
        result2 = install.acquire_repo(
            url=file_url,
            target=str(target_dir),
            git_enabled=False
        )
        self.assertTrue(result2)


class TestInvalidTargetAbort(unittest.TestCase):
    """Test error handling for invalid targets."""

    def test_acquire_repo_invalid_target_aborts(self):
        """Given: invalid target path, When: acquire_repo called, Then: raises error or returns False."""
        if not hasattr(install, 'acquire_repo'):
            self.skipTest("acquire_repo not implemented")
        
        # Use a path that cannot be created (e.g., inside a file)
        temp_dir = tempfile.mkdtemp()
        try:
            # Create a file where we'll try to create a directory
            blocking_file = Path(temp_dir) / "blocking"
            blocking_file.write_text("test")
            
            # Try to use a path inside the file as target
            invalid_target = str(blocking_file / "subdir")
            
            result = install.acquire_repo(
                url="file:///nonexistent.tar.gz",
                target=invalid_target,
                git_enabled=False
            )
            
            # Should fail gracefully
            self.assertFalse(result)
        finally:
            shutil.rmtree(temp_dir, ignore_errors=True)

    def test_acquire_repo_nonexistent_url_aborts(self):
        """Given: nonexistent URL, When: acquire_repo called, Then: raises error or returns False."""
        if not hasattr(install, 'acquire_repo'):
            self.skipTest("acquire_repo not implemented")
        
        temp_dir = tempfile.mkdtemp()
        try:
            target_dir = Path(temp_dir) / "target"
            target_dir.mkdir()
            
            result = install.acquire_repo(
                url="file:///nonexistent/path/to/tarball.tar.gz",
                target=str(target_dir),
                git_enabled=False
            )
            
            # Should fail gracefully
            self.assertFalse(result)
        finally:
            shutil.rmtree(temp_dir, ignore_errors=True)


class TestBootstrapIntegration(unittest.TestCase):
    """Integration tests for bootstrap workflow."""

    def setUp(self):
        """Create temporary directories for testing."""
        self.temp_dir = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.temp_dir, ignore_errors=True)

    def test_bootstrap_workflow_parse_and_derive(self):
        """Given: bootstrap args, When: parsed and tarball_url derived, Then: workflow succeeds."""
        if not hasattr(install, 'parse_bootstrap_args') or not hasattr(install, 'tarball_url'):
            self.skipTest("parse_bootstrap_args or tarball_url not implemented")
        
        args = install.parse_bootstrap_args([
            '--repo=https://github.com/org/repo',
            '--branch=main'
        ])
        
        url = install.tarball_url(
            repo=args.get('repo'),
            branch=args.get('branch'),
            tag=args.get('tag')
        )
        
        self.assertIsNotNone(url)
        self.assertIn('github.com', url)

    def test_bootstrap_workflow_with_no_git(self):
        """Given: --no-git flag, When: bootstrap workflow runs, Then: git_enabled is False."""
        if not hasattr(install, 'parse_bootstrap_args'):
            self.skipTest("parse_bootstrap_args not implemented")
        
        args = install.parse_bootstrap_args(['--no-git'])

        self.assertFalse(args.get('git_enabled', True))

    @patch.object(install.shutil, 'which', return_value=None)
    @patch.object(install.subprocess, 'run')
    @patch('builtins.input', return_value='n')
    def test_ensure_rtk_installed_prompts_when_missing(self, mock_input, mock_run, mock_which):
        """Given: rtk is missing, When: ensure_rtk_installed is called, Then: it prompts and skips on no."""
        if not hasattr(install, 'ensure_rtk_installed'):
            self.skipTest("ensure_rtk_installed not implemented")

        result = install.ensure_rtk_installed()

        self.assertFalse(result)
        mock_input.assert_called_once()
        mock_run.assert_not_called()


if __name__ == '__main__':
    unittest.main()
