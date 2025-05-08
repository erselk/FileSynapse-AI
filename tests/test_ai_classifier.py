import pytest
import os
import json
from src.core.ai_classifier import AIClassifier

@pytest.fixture
def classifier():
    return AIClassifier()

@pytest.fixture
def sample_file_info():
    return {
        'path': 'test.pdf',
        'name': 'test.pdf',
        'extension': '.pdf',
        'mime_type': 'application/pdf',
        'size': 1024,
        'content': 'This is a test document about invoices and reports.'
    }

def test_classifier_initialization(classifier):
    assert classifier is not None
    assert classifier.category_mappings is not None
    assert 'document' in classifier.category_mappings
    assert 'media' in classifier.category_mappings
    assert 'code' in classifier.category_mappings
    assert 'design' in classifier.category_mappings
    assert 'archive' in classifier.category_mappings

def test_classify_by_extension(classifier, sample_file_info):
    # Test PDF classification
    assert classifier._classify_by_extension('.pdf') == 'document'
    
    # Test image classification
    assert classifier._classify_by_extension('.jpg') == 'media'
    assert classifier._classify_by_extension('.png') == 'media'
    
    # Test code classification
    assert classifier._classify_by_extension('.py') == 'code'
    assert classifier._classify_by_extension('.js') == 'code'
    
    # Test design file classification
    assert classifier._classify_by_extension('.psd') == 'design'
    assert classifier._classify_by_extension('.ai') == 'design'
    
    # Test archive classification
    assert classifier._classify_by_extension('.zip') == 'archive'
    assert classifier._classify_by_extension('.rar') == 'archive'
    
    # Test unknown extension
    assert classifier._classify_by_extension('.xyz') is None

def test_classify_by_mime(classifier):
    # Test PDF classification
    assert classifier._classify_by_mime('application/pdf') == 'document'
    
    # Test image classification
    assert classifier._classify_by_mime('image/jpeg') == 'media'
    assert classifier._classify_by_mime('image/png') == 'media'
    
    # Test code classification
    assert classifier._classify_by_mime('text/x-python') == 'code'
    assert classifier._classify_by_mime('text/javascript') == 'code'
    
    # Test unknown MIME type
    assert classifier._classify_by_mime('application/unknown') is None

def test_classify_file(classifier, sample_file_info):
    # Test document classification
    result = classifier.classify_file(sample_file_info)
    assert result == 'document'
    
    # Test image classification
    sample_file_info['extension'] = '.jpg'
    sample_file_info['mime_type'] = 'image/jpeg'
    result = classifier.classify_file(sample_file_info)
    assert result == 'media'
    
    # Test code classification
    sample_file_info['extension'] = '.py'
    sample_file_info['mime_type'] = 'text/x-python'
    result = classifier.classify_file(sample_file_info)
    assert result == 'code'

def test_batch_classify(classifier):
    files_info = [
        {
            'path': 'doc.pdf',
            'name': 'doc.pdf',
            'extension': '.pdf',
            'mime_type': 'application/pdf'
        },
        {
            'path': 'image.jpg',
            'name': 'image.jpg',
            'extension': '.jpg',
            'mime_type': 'image/jpeg'
        },
        {
            'path': 'script.py',
            'name': 'script.py',
            'extension': '.py',
            'mime_type': 'text/x-python'
        }
    ]
    
    result = classifier.batch_classify(files_info)
    
    assert 'document' in result
    assert 'media' in result
    assert 'code' in result
    assert len(result['document']) == 1
    assert len(result['media']) == 1
    assert len(result['code']) == 1

def test_update_category_mappings(classifier, tmp_path):
    # Create a temporary category mappings file
    mappings_file = tmp_path / "category_mappings.json"
    
    new_mappings = {
        'test': {
            'keywords': ['test'],
            'extensions': ['.test'],
            'mime_types': ['application/test']
        }
    }
    
    # Update mappings
    classifier.update_category_mappings(new_mappings)
    
    # Verify the update
    assert 'test' in classifier.category_mappings
    assert '.test' in classifier.category_mappings['test']['extensions']
    assert 'application/test' in classifier.category_mappings['test']['mime_types']
    assert 'test' in classifier.category_mappings['test']['keywords'] 