import requests

def run_pagespeed_insights(url, api_key):
    api_url = f'https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url={url}&key={api_key}'
    response = requests.get(api_url)
    return response.json()

def generate_human_readable_report(pagespeed_result):
    # Extract relevant information
    performance_score = pagespeed_result['lighthouseResult']['categories']['performance']['score']
    loading_issues = pagespeed_result['loadingExperience']['overall_category']
    cumulative_layout_shift = pagespeed_result['lighthouseResult']['audits']['cumulative-layout-shift']['displayValue']
    first_contentful_paint = pagespeed_result['lighthouseResult']['audits']['first-contentful-paint']['displayValue']

    # Generate human-readable report
    report = f"Performance Score: {performance_score}\n"
    report += f"Loading Experience: {loading_issues}\n"
    report += f"Cumulative Layout Shift: {cumulative_layout_shift}\n"
    report += f"First Contentful Paint: {first_contentful_paint}\n"

    return report

# Example usage:
url_to_test = 'https://www.example.com'
pagespeed_api_key = 'AIzaSyACVDuVRHMBREEhrTKgdVvHpVY6VptYFxM'

pagespeed_result = run_pagespeed_insights(url_to_test, pagespeed_api_key)
print("PageSpeed Insights API Response:")
print(pagespeed_result)

print("\n--------------------\n")

# Generate and print the human-readable report
human_readable_report = generate_human_readable_report(pagespeed_result)
print("Human Readable Report:")
print(human_readable_report)
