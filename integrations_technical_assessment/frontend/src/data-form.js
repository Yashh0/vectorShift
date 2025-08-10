import { useState, useEffect } from 'react';
import {
    Box,
    TextField,
    Button,
} from '@mui/material';
import axios from 'axios';

const endpointMapping = {
    'Notion': 'notion',
    'Airtable': 'airtable',
    'HubSpot': 'hubspot',
};

export const DataForm = ({ integrationType, credentials }) => {
    const [loadedData, setLoadedData] = useState(null);
    const endpoint = endpointMapping[integrationType];

    const handleLoad = async () => {
        try {
            console.log(`🔄 Loading ${integrationType} data...`);
            const formData = new FormData();
            formData.append('credentials', JSON.stringify(credentials));
            const response = await axios.post(`http://localhost:8000/integrations/${endpoint}/load`, formData);
            const data = response.data;

            // Always log the full response and parsed data
            console.group(`${integrationType} Load Result`);
            console.log('Raw Axios response:', response);
            console.log('Parsed response data:', data);
            if (Array.isArray(data)) {
                console.log(`📊 Total items: ${data.length}`);
                console.table(data.map((item) => ({ id: item.id, name: item.name, type: item.type })));
            }
            // Expose for manual inspection in DevTools
            window.lastLoadedData = data;
            console.log('↪️ Inspect in DevTools via window.lastLoadedData');
            console.groupEnd();

            setLoadedData(data);
        } catch (e) {
            console.error(`❌ Error loading ${integrationType} data:`, e?.response?.data || e);
            alert(e?.response?.data?.detail);
        }
    }

    // Log whenever loadedData state changes
    useEffect(() => {
        if (loadedData) {
            console.log('✅ loadedData state updated:', loadedData);
        }
    }, [loadedData]);

    // Format data for display
    const formatDataForDisplay = (data) => {
        if (!data) return '';
        if (Array.isArray(data)) {
            return data.map((item, index) => {
                return `${index + 1}. ${item.name || item.id || 'Unnamed Item'} (${item.type || 'Unknown Type'})`;
            }).join('\n');
        }
        return JSON.stringify(data, null, 2);
    };

    return (
        <Box display='flex' justifyContent='center' alignItems='center' flexDirection='column' width='100%'>
            <Box display='flex' flexDirection='column' width='100%'>
                <TextField
                    label="Loaded Data"
                    value={formatDataForDisplay(loadedData)}
                    sx={{mt: 2}}
                    InputLabelProps={{ shrink: true }}
                    multiline
                    rows={8}
                    disabled
                />
                <Button
                    onClick={handleLoad}
                    sx={{mt: 2}}
                    variant='contained'
                >
                    Load Data
                </Button>
                <Button
                    onClick={() => setLoadedData(null)}
                    sx={{mt: 1}}
                    variant='contained'
                >
                    Clear Data
                </Button>
            </Box>
        </Box>
    );
}
