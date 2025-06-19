namespace Game;

/// @class RoomPage
/// @brief Class managing the game room interface
/// @details Handles the display and interaction of players in a game room,
///          including room management and navigation
public partial class RoomPage : ContentPage
{
    /// @brief Gets the list of players in the room
    /// @details Read-only collection of player names currently in the room
    public IReadOnlyList<string> Players { get; private set; }

    /// @brief Constructor for RoomPage
    /// @param players List of player names to initialize the room with
    /// @details Initializes the room components and sets up player list
    public RoomPage(List<string> players)
    {
        InitializeComponent();
        Players = players;
        BindingContext = this;
    }

    /// @brief Event handler for the start game button
    /// @param sender The object that triggered the event
    /// @param e The event arguments
    /// @details Navigates to the live map page to start the game
    private async void OnStartClicked(object sender, EventArgs e)
    {
        await Navigation.PushModalAsync(new NavigationPage(new LiveMapPage()));
    }

    /// @brief Event handler for the back button
    /// @param sender The object that triggered the event
    /// @param e The event arguments
    /// @details Returns to the previous page
    private async void OnBackClicked(object sender, EventArgs e)
    {
        await Navigation.PopModalAsync();
    }
}