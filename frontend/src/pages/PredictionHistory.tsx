import React, { useEffect, useState } from 'react';
import {
  Box,
  Card,
  CardContent,
  Grid,
  Typography,
  Container,
  CircularProgress,
  Alert,
  Chip,
} from '@mui/material';
import { useAuth } from '../contexts/AuthContext';
import axios from 'axios';
import { format } from 'date-fns';

interface Prediction {
  id: string;
  disease_name: string;
  confidence: number;
  timestamp: string;
  filename: string;
}

const PredictionHistory: React.FC = () => {
  const [predictions, setPredictions] = useState<Prediction[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const { token } = useAuth();

  useEffect(() => {
    const fetchPredictions = async () => {
      try {
        const response = await axios.get('http://localhost:8001/api/v1/predictions/history', {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        });
        setPredictions(response.data.predictions);
        setError('');
      } catch (err) {
        console.error('Error fetching prediction history:', err);
        setError('Failed to load prediction history. Please try again later.');
      } finally {
        setLoading(false);
      }
    };

    fetchPredictions();
  }, [token]);

  if (loading) {
    return (
      <Container sx={{ display: 'flex', justifyContent: 'center', mt: 4 }}>
        <CircularProgress />
      </Container>
    );
  }

  return (
    <Container maxWidth="md" sx={{ py: 4 }}>
      <Typography variant="h4" component="h1" gutterBottom align="center">
        Your Prediction History
      </Typography>

      {error && (
        <Alert severity="error" sx={{ mb: 4 }}>
          {error}
        </Alert>
      )}

      {predictions.length === 0 ? (
        <Card>
          <CardContent>
            <Typography variant="body1" align="center">
              You haven't made any predictions yet. Try analyzing some plant images!
            </Typography>
          </CardContent>
        </Card>
      ) : (
        <Grid container spacing={3}>
          {predictions.map((prediction) => (
            <Grid item xs={12} sm={6} md={4} key={prediction.id}>
              <Card>
                <CardContent>
                  <Typography variant="h6" gutterBottom>
                    {prediction.disease_name}
                  </Typography>
                  <Box sx={{ mb: 2 }}>
                    <Chip 
                      label={`${(prediction.confidence * 100).toFixed(1)}% confidence`}
                      color={prediction.confidence > 0.7 ? "success" : "warning"}
                      size="small"
                    />
                  </Box>
                  <Typography variant="body2" color="text.secondary">
                    File: {prediction.filename}
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    Date: {format(new Date(prediction.timestamp), 'PPp')}
                  </Typography>
                </CardContent>
              </Card>
            </Grid>
          ))}
        </Grid>
      )}
    </Container>
  );
};

export default PredictionHistory; 