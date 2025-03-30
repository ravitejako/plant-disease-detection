import React from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Box,
  Button,
  Card,
  CardContent,
  Container,
  Grid,
  Typography,
} from '@mui/material';
import CameraAltIcon from '@mui/icons-material/CameraAlt';
import BiotechIcon from '@mui/icons-material/Biotech';
import LocalHospitalIcon from '@mui/icons-material/LocalHospital';

const Home: React.FC = () => {
  const navigate = useNavigate();

  const features = [
    {
      icon: <CameraAltIcon fontSize="large" color="primary" />,
      title: 'Easy Image Upload',
      description: 'Simply upload a photo of your plant leaf to get started with the diagnosis.',
    },
    {
      icon: <BiotechIcon fontSize="large" color="primary" />,
      title: 'AI-Powered Analysis',
      description: 'Advanced machine learning algorithms analyze your plant for diseases with high accuracy.',
    },
    {
      icon: <LocalHospitalIcon fontSize="large" color="primary" />,
      title: 'Treatment Recommendations',
      description: 'Get detailed treatment suggestions and preventive measures for identified diseases.',
    },
  ];

  return (
    <Box>
      {/* Hero Section */}
      <Box
        sx={{
          bgcolor: 'background.paper',
          pt: 8,
          pb: 6,
          textAlign: 'center',
        }}
      >
        <Container maxWidth="sm">
          <Typography
            component="h1"
            variant="h2"
            color="text.primary"
            gutterBottom
          >
            Plant Disease Detection
          </Typography>
          <Typography variant="h5" color="text.secondary" paragraph>
            Protect your crops with AI-powered disease detection. Upload a photo of
            your plant and get instant diagnosis and treatment recommendations.
          </Typography>
          <Button
            variant="contained"
            size="large"
            onClick={() => navigate('/predict')}
            sx={{ mt: 4 }}
          >
            Start Detection
          </Button>
        </Container>
      </Box>

      {/* Features Section */}
      <Container sx={{ py: 8 }} maxWidth="md">
        <Grid container spacing={4}>
          {features.map((feature, index) => (
            <Grid item key={index} xs={12} sm={6} md={4}>
              <Card
                sx={{
                  height: '100%',
                  display: 'flex',
                  flexDirection: 'column',
                  alignItems: 'center',
                  textAlign: 'center',
                }}
              >
                <CardContent>
                  <Box sx={{ mb: 2 }}>{feature.icon}</Box>
                  <Typography gutterBottom variant="h5" component="h2">
                    {feature.title}
                  </Typography>
                  <Typography color="text.secondary">
                    {feature.description}
                  </Typography>
                </CardContent>
              </Card>
            </Grid>
          ))}
        </Grid>
      </Container>
    </Box>
  );
};

export default Home; 