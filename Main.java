import java.util.ArrayList;
import java.util.Iterator;
import java.util.List;
import java.util.Random;

import javafx.animation.AnimationTimer;
import javafx.animation.KeyFrame;
import javafx.animation.Timeline;
import javafx.application.Application;
import javafx.application.Platform;
import javafx.scene.Scene;
import javafx.scene.control.Button;
import javafx.scene.input.KeyCode;
import javafx.scene.input.KeyEvent;
import javafx.scene.layout.Pane;
import javafx.scene.paint.Color;
import javafx.scene.shape.Circle;
import javafx.scene.shape.Rectangle;
import javafx.scene.text.Font;
import javafx.scene.text.Text;
import javafx.stage.Stage;
import javafx.util.Duration;

public class Main extends Application{
	
	private Pane p;
	private Pane startScreen;
	private Button playButton;
	private Rectangle player;
	private List<Rectangle> cubes;
	private List<Circle> topLayerCircle;
	private List<Circle> bottomLayerCircle;
	private Random random = new Random();
	private Text gameOverText;
	private int scoreVal = 0;
	private Text scoreText;
	private Scene scene;
	private boolean gameOver = false;
	private double topLayerSpeedMultiplier = .80;
	private double bottomLayerSpeedMultiplier = .6; 
	private static final double player_speed = 9.0;
	private boolean moveLeft = false;
	private boolean moveRight = false;
	

	public static void main(String[] args) {
		launch(args);
	}

	@Override
	public void start(Stage primaryStage) throws Exception {
		p = new Pane();
		p.setStyle("-fx-background-color: black;");
		
		startScreen = new Pane();
		startScreen.setStyle("-fx-background-color: black;");
		
		Text titleText = new Text("Cube Field");
		titleText.setFont(Font.font("Roboto", 75));
		titleText.setFill(Color.RED);
		titleText.setX(420);
		titleText.setY(300);
		startScreen.getChildren().add(titleText);
		
		playButton = new Button("PLAY!");
		playButton.setFont(Font.font("Roboto", 50));
		playButton.setTextFill(Color.RED);
		playButton.setLayoutX(500);
		playButton.setLayoutY(400);
		playButton.setOnAction(e -> {primaryStage.setScene(scene);
									 initializeGame();});
		
		startScreen.getChildren().add(playButton);
		
		Scene startScene = new Scene(startScreen, 1200, 700);
		scene = new Scene(p, 1200, 700);
		
		primaryStage.setScene(startScene);
		primaryStage.setTitle("Cube Field");
		primaryStage.show();
		
		//creates the player cube
		player = new Rectangle(20, 20, Color.BLUE);
		player.setY(550);
		player.setX(200);
		
		//sets up the game scene
		cubes = new ArrayList<>();
		topLayerCircle = new ArrayList<>();
		bottomLayerCircle = new ArrayList<>();
		
		gameOverText = new Text();
		gameOverText.setFont(Font.font("Roboto", 50));
		gameOverText.setFill(Color.BLUE);
		gameOverText.setX(600);
		gameOverText.setY(350);
		
		scoreText = new Text("Score: 0");
		scoreText.setFont(Font.font("Roboto", 20));
		scoreText.setFill(Color.WHITE);
		scoreText.setX(10);
		scoreText.setY(30);
		
		//adds the player and score to the screen
		p.getChildren().add(scoreText);
		p.getChildren().addAll(player);

		//event handlers for key input
		player.requestFocus();
		scene.setOnKeyPressed(e -> handleKeyPress(e));
	    scene.setOnKeyReleased(e -> handleKeyRelease(e));
	    
	    
	    	// animation timer updates the game
	    	new AnimationTimer() {
		    @Override
		    public void handle(long timer) {
		    	if(!gameOver) {
		        updateGame();
		        movePlayer();
		    		}
		    	}
	    	}
	    	.start();
		}
	
		private void initializeGame() {
		    player.setX(200);
		    player.setY(550);
		    
		    scoreVal = 0;
		    updateScore();

		    p.getChildren().removeAll(cubes);
		    p.getChildren().removeAll(topLayerCircle);
		    p.getChildren().removeAll(bottomLayerCircle);

		    gameOverText.setVisible(false);
		    p.getChildren().remove(gameOverText);
		    p.getChildren().removeAll(cubes);

		    gameOver = false;
		}

		//checks if the arrow keys are being used
		private void handleKeyPress(KeyEvent event) {
		    if (event.getCode() == KeyCode.LEFT) {
		        moveLeft = true;
		    } else if (event.getCode() == KeyCode.RIGHT) {
		        moveRight = true;
		    }
		}
		
		//checks if the arrow keys are not being used
		private void handleKeyRelease(KeyEvent event) {
		    if (event.getCode() == KeyCode.LEFT) {
		        moveLeft = false;
		    } else if (event.getCode() == KeyCode.RIGHT) {
		        moveRight = false;
		    }
		}

		
	
	private void updateGame() {
		//updates state of the game
		if(gameOver) {
			return;
	}
		//randomly generates cubes and stars for the background
		if(random.nextInt(100) < 20) {
			generateCube();
	}
		if(random.nextInt(100) < 50) {
			generateTopLayerCircle();
	}
		if(random.nextInt(100) < 60) {
			generateBottomLayerCircle();
	}
		
	// adds speed while the game goes on
	double speedMultiplier = 1.0 + scoreVal/2000.0;
	//checks for collisions with the player and removes cubes that are off the screen
	// also gives red cubes their movement 
    Iterator<Rectangle> iterator = cubes.iterator();{	// Create an iterator for the 'cubes' collection of Rectangle objects
    while (iterator.hasNext()) {	// Iterate through each cube in the collection
        Rectangle cube = iterator.next();	// Get the next cube in the iteration
        if (cube.getBoundsInParent().intersects(player.getBoundsInParent())) {	    // Check if the bounding box of the cube intersects with the player's bounding box
            gameOver();  // If there is an intersection, invoke the gameOver() method
        }
        //calls update score as cubes pass the player
        if (cube.getY() > p.getHeight()) {
            iterator.remove();
            p.getChildren().remove(cube);
            updateScore();
        }
        //uses the speedMultiplier to make the game more difficult the higher the players score
        cube.setY(cube.getY() + 3 * speedMultiplier);
    }
    	 
        Iterator<Circle> topLayerIterator = topLayerCircle.iterator();
            while (topLayerIterator.hasNext()) {
                Circle circle = topLayerIterator.next();
                circle.setCenterY(circle.getCenterY() + 3 * topLayerSpeedMultiplier);
                
                if (circle.getCenterY() > p.getHeight()) {
                	topLayerIterator.remove();
                	p.getChildren().remove(circle);
                	}
            	}
    	Iterator<Circle> bottomLayerIterator = bottomLayerCircle.iterator();
            while (bottomLayerIterator.hasNext()) {
                Circle circle = bottomLayerIterator.next();
                circle.setCenterY(circle.getCenterY() + 3 * bottomLayerSpeedMultiplier);

                if (circle.getCenterY() > p.getHeight()) {
                    bottomLayerIterator.remove();
                    p.getChildren().remove(circle);
                	}
                }
    		}
		}
    //adds 10 to score and displays it at the top of the screen
	private void updateScore() {
		scoreVal += 10;
		scoreText.setText("score: " + scoreVal);
	}
	
	// creates red cubes
	private void generateCube() {
		Rectangle cube = new Rectangle(20, 20, Color.RED);
		cube.setX(random.nextDouble() * (p.getWidth() - cube.getWidth()));
		cube.setY(-cube.getHeight());
		cubes.add(cube);
		p.getChildren().add(cube);
	}
	
	//creates star for background
	private void generateTopLayerCircle() {
		Circle circle = new Circle(1, Color.WHITE);
		circle.setCenterX(random.nextDouble() * p.getWidth());
		circle.setCenterY(-circle.getRadius());
		topLayerCircle.add(circle);
		p.getChildren().add(circle);
	}
	
	//creates star for background
	private void generateBottomLayerCircle() {
        Circle circle = new Circle(1, Color.WHITE);
        circle.setCenterX(random.nextDouble() * p.getWidth());
        circle.setCenterY(-circle.getRadius());
        bottomLayerCircle.add(circle);
        p.getChildren().add(circle);
    }
	
	// prints game over when player collides with a red cube 
	// also closes the screen after the game has ended
	private void gameOver() {
		gameOverText.setText("Game Over\nScore: " + scoreVal);
		gameOverText.setVisible(true);
		gameOver = true;
		p.getChildren().add(gameOverText);
		Timeline timeline = new Timeline(new KeyFrame(Duration.seconds(5), event -> Platform.exit()));
		timeline.play();
	}
	
	//uses the playerSpeed to move the player
	private void movePlayer() {
		if (moveLeft) {
			double x = player.getX();
			if(x - player_speed >= 0) {
				player.setX(x - player_speed);
			}
		}
		 if (moveRight) {
			double x = player.getX();
	        if (x + player.getWidth() + player_speed <= p.getWidth()) {
	            player.setX(x + player_speed);
	        }
		 }
	}
}

