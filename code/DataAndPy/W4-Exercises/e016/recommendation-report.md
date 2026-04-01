# Scope
Your company is a mid-sized e-commerce retailer planning to migrate their on-premises data infrastructure to the cloud. They need to:

1. Store transactional data from their PostgreSQL database
2. Build a data warehouse for business analytics
3. Process daily batch jobs for inventory management
4. Store product images and customer documents
5. Eventually implement real-time analytics for fraud detection

Leadership has asked you to evaluate AWS, Azure, and GCP and provide a recommendation.

# Executive Summary
The following presents a cost-benefit analysis of AWS, Azure, and GCP cloud services in Company XYZ's migration from on-premises infrastructure. This report will provide evaluation criteria, strengths and weaknesses of each service, a recommendation with reasoning, and migration considerations

# Evaluation Criteria
1. Storage Size - 
Size requirements are relatively small at Company XYZ's current level. It would be wise to choose a cloud service that has pricing options for our set, but also offers room to grow.
2. Data Access Frequency - 
Each provider has different tiers and add-ons bases on access frequency. Pricing will vary differently based on how we use the storage instances.
3. Analytics & Real-Time Processing - 
The chosen cloud provider should be able to implement real-time analytics for fraud detection, as it is one of Company XYZ's requirements. 
4. Integration & Migration Ease - 
Company XYZ is looking to move the current infrastructure entirely to cloud providers. A provider that easily allows on-premises to cloud migration, and cloud-to-cloud migration (in case needs expand) is important.
5. Scalability & Cost Over Time - 
We must consider how this data will be used in the future. Will the dataset expand? Will more queries be required? Anticipating future needs is critical in selecting the best provider to use.

# Provider Comparison
|Provider|Strengths|Weaknesses|
|----|----|----|
|AWS|breadth of services, market share| complex pricing
|Azure|enterprise integration, MS ecosystem| most expensive
|GCP|best analytics, simpler pricing| smaller talent pool

# Recommendation
On cost alone, Google Cloud Platform is the best option. They have the analytics and scalability we need. We could take advantage of the Google Suite for our team's daily operations, and they have great documentation and an easy to understand interface.

As Company XYZ grows, the needs might shift to require the more specific services needed by AWS or Azure, but GCP is currently the best option for our needs.

# Migration Considerations
1. Expertise - 
Company XYZ should ensure they have a team of experts facilitating the migration. Diligence in security administration and cost optimization will ensure our cloud provider is utilized effectively. Mistakes in migration or operation could be costly. Spending to ensure handlers are properly trained is worth it in the long-term.
2. Vendor lock-in - 
As Company XYZ grow, vender lock-in becomes a larger risk. It's important to keep this mind for future cloud considerations. 
3. Cost management - 
Costs can add up quickly in cloud computing. Company XYZ should pay attention to these cost drivers when migrating to the cloud.
    - **Compute**: Running instances 24/7 when not needed
    - **Storage**: Accumulating data without lifecycle policies
    - **Data Transfer**: Egress charges for moving data out
    - **Over-provisioning**: Using larger instances than necessary
    - **Zombie Resources**: Forgotten resources still running
