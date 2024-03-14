import * as React from 'react';
import Box from '@mui/material/Box';
import Card from '@mui/material/Card';
import CardActions from '@mui/material/CardActions';
import CardContent from '@mui/material/CardContent';
import Button from '@mui/material/Button';
import Typography from '@mui/material/Typography';
import { start } from 'repl';

export default function SuggestionCard(){
    return (
        <>
            <Card sx={{ width: 0.98 / 3, cursor: 'pointer' }} onClick = {() => {alert('yes')}}>
                <CardContent>
                    <Typography sx={{ fontSize: 15, textAlign: 'start'}} color="text.secondary" gutterBottom>
                        Kakuv e Kamen?
                    </Typography>
                </CardContent>
            </Card> 
        </>
    )
}