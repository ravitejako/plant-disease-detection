import React, { useState, useRef, useEffect } from 'react';
import { useDropzone } from 'react-dropzone';
import {
  Box,
  Button,
  Card,
  CardContent,
  CircularProgress,
  Container,
  Typography,
  List,
  ListItem,
  ListItemText,
  Alert,
  IconButton,
  Stack,
  Dialog,
  DialogContent,
  DialogTitle,
  DialogActions,
} from '@mui/material';
import CloudUploadIcon from '@mui/icons-material/CloudUpload';
import CameraAltIcon from '@mui/icons-material/CameraAlt';
import PhotoCameraIcon from '@mui/icons-material/PhotoCamera';
import FlipCameraIosIcon from '@mui/icons-material/FlipCameraIos';
import CloseIcon from '@mui/icons-material/Close';
import axios from 'axios';
import { useAuth } from '../contexts/AuthContext';

interface PredictionResult {
  disease_name: string;
  confidence: number;
  description: string;
  treatment_recommendations: string[];
  preventive_measures: string[];
}

const Predict: React.FC = () => {
  const { token } = useAuth();
  const [image, setImage] = useState<File | null>(null);
  const [preview, setPreview] = useState<string>('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string>('');
  const [result, setResult] = useState<PredictionResult | null>(null);
  const [isCameraOpen, setIsCameraOpen] = useState(false);
  const [isCameraLoading, setIsCameraLoading] = useState(false);
  const [cameraError, setCameraError] = useState<string>('');
  const videoRef = useRef<HTMLVideoElement>(null);
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const [stream, setStream] = useState<MediaStream | null>(null);
  const [facingMode, setFacingMode] = useState<'user' | 'environment'>('environment');

  // Cleanup function for camera resources
  useEffect(() => {
    return () => {
      if (stream) {
        stream.getTracks().forEach(track => track.stop());
      }
    };
  }, [stream]);

  const onDrop = (acceptedFiles: File[]) => {
    const file = acceptedFiles[0];
    setImage(file);
    setPreview(URL.createObjectURL(file));
    setError('');
    setResult(null);
  };

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'image/*': ['.jpeg', '.jpg', '.png']
    },
    multiple: false,
  });

  const startCamera = async () => {
    setIsCameraLoading(true);
    setCameraError('');
    try {
      // First check if the browser supports getUserMedia
      if (!navigator.mediaDevices?.getUserMedia) {
        throw new Error('Your browser does not support camera access');
      }

      // Stop any existing stream
      if (stream) {
        stream.getTracks().forEach(track => track.stop());
      }

      // Get list of available cameras
      const devices = await navigator.mediaDevices.enumerateDevices();
      const videoDevices = devices.filter(device => device.kind === 'videoinput');

      // If no cameras are found
      if (videoDevices.length === 0) {
        throw new Error('No camera devices found');
      }

      const mediaStream = await navigator.mediaDevices.getUserMedia({
        video: {
          facingMode: facingMode,
          width: { ideal: 1920 },
          height: { ideal: 1080 }
        }
      });

      setStream(mediaStream);
      if (videoRef.current) {
        videoRef.current.srcObject = mediaStream;
      }
      setIsCameraOpen(true);
      setCameraError('');
    } catch (err) {
      console.error('Camera error:', err);
      setCameraError(
        err instanceof Error 
          ? err.message 
          : 'Error accessing camera. Please make sure you have granted camera permissions.'
      );
    } finally {
      setIsCameraLoading(false);
    }
  };

  const toggleCamera = async () => {
    setFacingMode(prev => prev === 'user' ? 'environment' : 'user');
    await startCamera();
  };

  const stopCamera = () => {
    if (stream) {
      stream.getTracks().forEach(track => track.stop());
      setStream(null);
    }
    setIsCameraOpen(false);
    setCameraError('');
  };

  const captureImage = () => {
    if (videoRef.current && canvasRef.current) {
      const video = videoRef.current;
      const canvas = canvasRef.current;
      
      // Set canvas dimensions to match video
      canvas.width = video.videoWidth;
      canvas.height = video.videoHeight;
      
      // Draw video frame to canvas
      const context = canvas.getContext('2d');
      if (context) {
        if (facingMode === 'user') {
          // Flip horizontally for front camera
          context.scale(-1, 1);
          context.drawImage(video, -canvas.width, 0, canvas.width, canvas.height);
        } else {
          context.drawImage(video, 0, 0, canvas.width, canvas.height);
        }
        
        // Convert canvas to file
        canvas.toBlob((blob) => {
          if (blob) {
            const file = new File([blob], 'camera-capture.jpg', { type: 'image/jpeg' });
            setImage(file);
            setPreview(URL.createObjectURL(file));
            stopCamera();
          }
        }, 'image/jpeg', 0.9); // 0.9 quality for better file size
      }
    }
  };

  const handleSubmit = async () => {
    if (!image) return;

    setLoading(true);
    setError('');
    setResult(null);

    const formData = new FormData();
    formData.append('file', image);

    try {
      const response = await axios.post('http://localhost:8001/api/v1/predict', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
          'Authorization': `Bearer ${token}`
        },
      });
      setResult(response.data);
    } catch (err) {
      setError('Error processing image. Please try again.');
      console.error('Error:', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Container maxWidth="md">
      <Typography variant="h4" gutterBottom align="center">
        Detect Plant Disease
      </Typography>
      
      {/* Upload Section */}
      <Card sx={{ mb: 4 }}>
        <CardContent>
          <Stack direction="row" spacing={2} justifyContent="center" mb={3}>
            <Button
              variant="contained"
              startIcon={<CameraAltIcon />}
              onClick={startCamera}
              disabled={isCameraLoading}
            >
              {isCameraLoading ? 'Starting Camera...' : 'Take Picture'}
            </Button>
            <Button
              variant="outlined"
              startIcon={<CloudUploadIcon />}
              {...getRootProps()}
            >
              Upload Image
              <input {...getInputProps()} />
            </Button>
          </Stack>

          {/* Camera Dialog */}
          <Dialog 
            open={isCameraOpen} 
            onClose={stopCamera}
            maxWidth="sm"
            fullWidth
          >
            <DialogTitle>
              Take a Picture
              <IconButton
                onClick={stopCamera}
                sx={{ position: 'absolute', right: 8, top: 8 }}
              >
                <CloseIcon />
              </IconButton>
            </DialogTitle>
            <DialogContent>
              {cameraError ? (
                <Alert severity="error" sx={{ mb: 2 }}>
                  {cameraError}
                </Alert>
              ) : (
                <Box sx={{ position: 'relative', width: '100%' }}>
                  <video
                    ref={videoRef}
                    autoPlay
                    playsInline
                    style={{
                      width: '100%',
                      height: 'auto',
                      transform: facingMode === 'user' ? 'scaleX(-1)' : 'none'
                    }}
                  />
                  <Stack
                    direction="row"
                    spacing={2}
                    sx={{
                      position: 'absolute',
                      bottom: 16,
                      left: '50%',
                      transform: 'translateX(-50%)',
                    }}
                  >
                    <IconButton
                      sx={{
                        backgroundColor: 'primary.main',
                        '&:hover': { backgroundColor: 'primary.dark' },
                      }}
                      onClick={toggleCamera}
                    >
                      <FlipCameraIosIcon sx={{ color: 'white' }} />
                    </IconButton>
                    <IconButton
                      sx={{
                        backgroundColor: 'primary.main',
                        '&:hover': { backgroundColor: 'primary.dark' },
                      }}
                      onClick={captureImage}
                    >
                      <PhotoCameraIcon sx={{ color: 'white' }} />
                    </IconButton>
                  </Stack>
                  <canvas ref={canvasRef} style={{ display: 'none' }} />
                </Box>
              )}
            </DialogContent>
            <DialogActions>
              <Button onClick={stopCamera}>Cancel</Button>
            </DialogActions>
          </Dialog>

          {preview && (
            <Box sx={{ textAlign: 'center' }}>
              <img
                src={preview}
                alt="Preview"
                style={{
                  maxWidth: '100%',
                  maxHeight: '300px',
                  objectFit: 'contain',
                }}
              />
              <Button
                variant="contained"
                onClick={handleSubmit}
                disabled={loading}
                sx={{ mt: 2 }}
              >
                {loading ? <CircularProgress size={24} /> : 'Analyze Image'}
              </Button>
            </Box>
          )}
        </CardContent>
      </Card>

      {/* Error Message */}
      {error && (
        <Alert severity="error" sx={{ mb: 4 }}>
          {error}
        </Alert>
      )}

      {/* Results Section */}
      {result && (
        <Card>
          <CardContent>
            <Typography variant="h5" gutterBottom>
              Detection Results
            </Typography>
            
            <Typography variant="h6" color="primary" gutterBottom>
              {result.disease_name}
            </Typography>
            
            <Typography variant="body1" gutterBottom>
              Confidence: {(result.confidence * 100).toFixed(2)}%
            </Typography>
            
            <Typography variant="body1" paragraph>
              {result.description}
            </Typography>

            <Typography variant="h6" gutterBottom>
              Treatment Recommendations
            </Typography>
            <List>
              {result.treatment_recommendations.map((treatment, index) => (
                <ListItem key={index}>
                  <ListItemText primary={treatment} />
                </ListItem>
              ))}
            </List>

            <Typography variant="h6" gutterBottom>
              Preventive Measures
            </Typography>
            <List>
              {result.preventive_measures.map((measure, index) => (
                <ListItem key={index}>
                  <ListItemText primary={measure} />
                </ListItem>
              ))}
            </List>
          </CardContent>
        </Card>
      )}
    </Container>
  );
};

export default Predict; 