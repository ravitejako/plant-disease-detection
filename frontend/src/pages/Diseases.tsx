import React, { useEffect, useState } from 'react';
import {
  Container,
  Typography,
  Grid,
  Card,
  CardContent,
  Accordion,
  AccordionSummary,
  AccordionDetails,
  CircularProgress,
  Alert,
} from '@mui/material';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import axios from 'axios';
import { useAuth } from '../contexts/AuthContext';

interface Disease {
  name: string;
  description: string;
  symptoms: string[];
  treatments: string[];
  preventive_measures: string[];
}

const Diseases: React.FC = () => {
  const [diseases, setDiseases] = useState<Disease[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const { token } = useAuth();

  useEffect(() => {
    const fetchDiseases = async () => {
      try {
        const response = await axios.get('http://localhost:8001/api/v1/diseases', {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        });
        setDiseases(response.data.diseases);
        setError('');
      } catch (err) {
        console.error('Error fetching diseases:', err);
        setError('Failed to load disease information. Please try again later.');
      } finally {
        setLoading(false);
      }
    };

    fetchDiseases();
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
        Plant Disease Guide
      </Typography>

      {error && (
        <Alert severity="error" sx={{ mb: 4 }}>
          {error}
        </Alert>
      )}

      <Grid container spacing={3}>
        {diseases.map((disease) => (
          <Grid item xs={12} key={disease.name}>
            <Accordion>
              <AccordionSummary expandIcon={<ExpandMoreIcon />}>
                <Typography variant="h6">{disease.name}</Typography>
              </AccordionSummary>
              <AccordionDetails>
                <Typography paragraph>
                  <strong>Description:</strong> {disease.description}
                </Typography>

                <Typography variant="subtitle1" gutterBottom>
                  <strong>Symptoms:</strong>
                </Typography>
                <ul>
                  {disease.symptoms.map((symptom, index) => (
                    <li key={index}>
                      <Typography>{symptom}</Typography>
                    </li>
                  ))}
                </ul>

                <Typography variant="subtitle1" gutterBottom>
                  <strong>Treatments:</strong>
                </Typography>
                <ul>
                  {disease.treatments.map((treatment, index) => (
                    <li key={index}>
                      <Typography>{treatment}</Typography>
                    </li>
                  ))}
                </ul>

                <Typography variant="subtitle1" gutterBottom>
                  <strong>Preventive Measures:</strong>
                </Typography>
                <ul>
                  {disease.preventive_measures.map((measure, index) => (
                    <li key={index}>
                      <Typography>{measure}</Typography>
                    </li>
                  ))}
                </ul>
              </AccordionDetails>
            </Accordion>
          </Grid>
        ))}
      </Grid>
    </Container>
  );
};

export default Diseases; 