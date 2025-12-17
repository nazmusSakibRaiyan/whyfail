"""
Comprehensive tests for whyfail library.
"""
import pytest
import whyfail
from whyfail import Explanation
from io import StringIO
import sys


class TestExplanations:
    """Test explanation generation for various exception types."""
    
    def test_key_error_explanation(self):
        """Test KeyError explanation."""
        try:
            data = {"name": "John"}
            _ = data["age"]
        except KeyError as e:
            explanation = whyfail.get_explanation(e)
            assert explanation is not None
            assert "Missing dictionary key" in explanation
            assert "age" in explanation
    
    def test_index_error_explanation(self):
        """Test IndexError explanation."""
        try:
            my_list = [1, 2, 3]
            _ = my_list[10]
        except IndexError as e:
            explanation = whyfail.get_explanation(e)
            assert explanation is not None
            assert "List index out of range" in explanation
    
    def test_type_error_explanation(self):
        """Test TypeError explanation."""
        try:
            result = "hello" + 5
        except TypeError as e:
            explanation = whyfail.get_explanation(e)
            assert explanation is not None
            assert "Operation not supported" in explanation
    
    def test_value_error_explanation(self):
        """Test ValueError explanation."""
        try:
            value = int("not a number")
        except ValueError as e:
            explanation = whyfail.get_explanation(e)
            assert explanation is not None
            assert "Invalid value" in explanation
    
    def test_attribute_error_explanation(self):
        """Test AttributeError explanation."""
        try:
            obj = "string"
            _ = obj.nonexistent_method()
        except AttributeError as e:
            explanation = whyfail.get_explanation(e)
            assert explanation is not None
            assert "Object has no such attribute" in explanation
    
    def test_name_error_explanation(self):
        """Test NameError explanation."""
        try:
            _ = undefined_variable
        except NameError as e:
            explanation = whyfail.get_explanation(e)
            assert explanation is not None
            assert "not defined" in explanation
    
    def test_zero_division_error_explanation(self):
        """Test ZeroDivisionError explanation."""
        try:
            result = 10 / 0
        except ZeroDivisionError as e:
            explanation = whyfail.get_explanation(e)
            assert explanation is not None
            assert "divide by zero" in explanation
    
    def test_file_not_found_error_explanation(self):
        """Test FileNotFoundError explanation."""
        try:
            with open("/nonexistent/file.txt") as f:
                pass
        except FileNotFoundError as e:
            explanation = whyfail.get_explanation(e)
            assert explanation is not None
            assert "File not found" in explanation
    
    def test_import_error_explanation(self):
        """Test ImportError explanation."""
        try:
            import nonexistent_module_xyz
        except ImportError as e:
            explanation = whyfail.get_explanation(e)
            assert explanation is not None
            assert "cannot be imported" in explanation


class TestContextManager:
    """Test the explain() context manager."""
    
    def test_context_manager_catches_exception(self):
        """Test that context manager catches and re-raises exception."""
        with pytest.raises(KeyError):
            with whyfail.explain():
                data = {}
                _ = data["missing"]
    
    def test_context_manager_with_reraise_false(self):
        """Test context manager with reraise=False."""
        # Should not raise
        with whyfail.explain(reraise=False):
            data = {}
            _ = data["missing"]
    
    def test_context_manager_prints_explanation(self, capsys):
        """Test that context manager prints explanation."""
        try:
            with whyfail.explain():
                data = {}
                _ = data["missing"]
        except KeyError:
            pass
        
        captured = capsys.readouterr()
        assert "[WHYFAIL]" in captured.out
        assert "Missing dictionary key" in captured.out
    
    def test_context_manager_suppresses_traceback(self, capsys):
        """Test that traceback can be suppressed."""
        try:
            with whyfail.explain(show_traceback=False):
                data = {}
                _ = data["missing"]
        except KeyError:
            pass
        
        captured = capsys.readouterr()
        assert "Full traceback" not in captured.out
    
    def test_unknown_exception_no_explanation(self, capsys):
        """Test that unknown exception types get generic message."""
        class UnknownError(Exception):
            pass
        
        try:
            with whyfail.explain():
                raise UnknownError("test")
        except UnknownError:
            pass
        
        captured = capsys.readouterr()
        assert "[WHYFAIL]" in captured.out
        assert "No explanation available" in captured.out


class TestDecorator:
    """Test the explain_errors() decorator."""
    
    def test_decorator_catches_exception(self):
        """Test that decorator catches and re-raises exception."""
        @whyfail.explain_errors()
        def raises_key_error():
            data = {}
            return data["missing"]
        
        with pytest.raises(KeyError):
            raises_key_error()
    
    def test_decorator_with_reraise_false(self):
        """Test decorator with reraise=False."""
        @whyfail.explain_errors(reraise=False)
        def raises_key_error():
            data = {}
            return data["missing"]
        
        # Should not raise
        result = raises_key_error()
    
    def test_decorator_prints_explanation(self, capsys):
        """Test that decorator prints explanation."""
        @whyfail.explain_errors()
        def raises_key_error():
            data = {}
            return data["missing"]
        
        try:
            raises_key_error()
        except KeyError:
            pass
        
        captured = capsys.readouterr()
        assert "[WHYFAIL]" in captured.out
        assert "Missing dictionary key" in captured.out
    
    def test_decorator_preserves_function_metadata(self):
        """Test that decorator preserves function metadata."""
        @whyfail.explain_errors()
        def my_function():
            """This is my function."""
            pass
        
        assert my_function.__name__ == "my_function"
        assert "This is my function" in my_function.__doc__
    
    def test_decorator_with_args_and_kwargs(self):
        """Test that decorator works with function arguments."""
        @whyfail.explain_errors()
        def function_with_args(a, b, c=None):
            return a + b
        
        # Should work normally
        result = function_with_args(1, 2, c=3)
        assert result == 3


class TestExplainerRegistry:
    """Test custom explainer registration."""
    
    def test_register_custom_explainer(self):
        """Test registering a custom explainer."""
        class CustomError(Exception):
            pass
        
        def custom_explainer(err):
            return Explanation(
                title="Custom error",
                reason="This is a custom error",
                suggestions=["Fix it"]
            )
        
        whyfail.register_explainer(CustomError, custom_explainer)
        
        try:
            raise CustomError("test")
        except CustomError as e:
            explanation = whyfail.get_explanation(e)
            assert explanation is not None
            assert "Custom error" in explanation
    
    def test_get_explainer(self):
        """Test getting an explainer."""
        explainer = whyfail.get_explainer(KeyError)
        assert explainer is not None
        assert callable(explainer)
    
    def test_get_nonexistent_explainer(self):
        """Test getting explainer for unknown exception."""
        class UnknownError(Exception):
            pass
        
        explainer = whyfail.get_explainer(UnknownError)
        assert explainer is None


class TestConfiguration:
    """Test global configuration."""
    
    def test_configure_global_settings(self):
        """Test setting global configuration."""
        whyfail.configure(show_traceback=False, reraise=False)
        
        # Configuration should be applied
        with whyfail.explain():
            data = {}
            _ = data["missing"]
        
        # Should not raise due to reraise=False
    
    def test_local_config_overrides_global(self, capsys):
        """Test that local config overrides global."""
        whyfail.configure(show_traceback=False)
        
        try:
            with whyfail.explain(show_traceback=True):
                data = {}
                _ = data["missing"]
        except KeyError:
            pass
        
        captured = capsys.readouterr()
        assert "Full traceback" in captured.out


class TestExplanationModel:
    """Test the Explanation model."""
    
    def test_explanation_creation(self):
        """Test creating an Explanation."""
        exp = Explanation(
            title="Test title",
            reason="Test reason",
            suggestions=["Suggestion 1", "Suggestion 2"]
        )
        
        assert exp.title == "Test title"
        assert exp.reason == "Test reason"
        assert len(exp.suggestions) == 2
    
    def test_explanation_formatting(self):
        """Test explanation formatting."""
        exp = Explanation(
            title="Test title",
            reason="Test reason",
            suggestions=["Suggestion 1", "Suggestion 2"],
            context="Test context"
        )
        
        output = exp.format_output()
        assert "[WHYFAIL]" in output
        assert "Test title" in output
        assert "Test reason" in output
        assert "Suggestion 1" in output
        assert "Test context" in output
    
    def test_explanation_without_context(self):
        """Test explanation without context."""
        exp = Explanation(
            title="Test title",
            reason="Test reason",
            suggestions=["Suggestion 1"]
        )
        
        output = exp.format_output()
        assert "[WHYFAIL]" in output
        assert "Additional context" not in output


class TestUtilityFunctions:
    """Test utility functions."""
    
    def test_get_explanation_with_none(self):
        """Test get_explanation with None."""
        result = whyfail.get_explanation(None)
        # This might fail, but shouldn't crash
    
    def test_format_value_truncation(self):
        """Test that large values are truncated."""
        from whyfail.utils import format_value
        
        long_string = "a" * 200
        result = format_value(long_string, max_length=50)
        assert len(result) <= 50
        assert "..." in result
    
    def test_find_close_matches(self):
        """Test finding close string matches."""
        from whyfail.utils import find_close_matches
        
        candidates = ["name", "age", "email"]
        matches = find_close_matches("nam", candidates)
        assert "name" in matches


class TestIntegration:
    """Integration tests."""
    
    def test_nested_context_managers(self):
        """Test nested explain context managers."""
        with pytest.raises(KeyError):
            with whyfail.explain():
                with whyfail.explain():
                    data = {}
                    _ = data["missing"]
    
    def test_decorator_and_context_manager(self):
        """Test using decorator and context manager together."""
        @whyfail.explain_errors()
        def inner_function():
            with whyfail.explain(reraise=False):
                data = {}
                _ = data["missing"]
        
        # Should not raise due to inner context manager
        inner_function()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
