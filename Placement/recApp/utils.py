from django.db.models import Count
from .models import PlacedStudent

def get_placements_by_year():
    # Group by year and count the number of students placed
    placement_data = (
        PlacedStudent.objects.values('placed_year')
        .annotate(total=Count('id'))
        .order_by('placed_year')
    )
    return placement_data



import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

def plot_placements_by_year(data):
    # Convert data to Pandas DataFrame
    df = pd.DataFrame.from_records(data)
    
    # Plot
    plt.figure(figsize=(10, 6))
    sns.barplot(x='placed_year', y='total', data=df, palette='coolwarm')
    plt.title('Number of Students Placed Each Year')
    plt.xlabel('Year')
    plt.ylabel('Number of Students')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    
    # Save the plot to the static folder
    image_path = 'static/images/placements_by_year.png'
    plt.savefig(image_path)
    plt.close()  # Close the plot to free memory
    return image_path
