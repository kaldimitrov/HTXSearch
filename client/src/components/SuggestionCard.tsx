import Card from "@mui/material/Card";
import CardContent from "@mui/material/CardContent";
import Typography from "@mui/material/Typography";

export default function SuggestionCard(props: {
  text: string;
  updateValue: Function;
  theme: string;
}) {
  return (
    <>
      <Card
        sx={{
          width: 0.98 / 3,
          height: 1 / 4,
          cursor: "pointer",
          borderRadius: 3,
          boxShadow: 3,
          "&:hover": {
            transition: "background-color 0.5s",
            backgroundColor: props.theme == "light" ? "#FFAE00" : "#FF1A16",
          },
        }}
        onClick={() => props.updateValue(props.text)}
      >
        <CardContent>
          <Typography
            sx={{ fontSize: "1.25rem", textAlign: "start" }}
            color="text.secondary"
            gutterBottom
          >
            {props.text}
          </Typography>
        </CardContent>
      </Card>
    </>
  );
}
