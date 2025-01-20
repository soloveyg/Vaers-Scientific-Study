CREATE TABLE [VDATA](
	[VAERS_ID] [int] NOT NULL,
	[RECVDATE] [datetime] NULL,
	[STATE] [nvarchar](max) NULL,
	[AGE_YRS] [decimal](5, 2) NULL,
	[CAGE_YR] [decimal](5, 2) NULL,
	[CAGE_MO] [decimal](5, 2) NULL,
	[SEX] [nvarchar](1) NULL,
	[RPT_DATE] [datetime] NULL,
	[SYMPTOM_TEXT] [nvarchar](max) NULL,
	[DIED] [bit] NULL,
	[DATEDIED] [datetime] NULL,
	[L_THREAT] [bit] NULL,
	[ER_VISIT] [bit] NULL,
	[HOSPITAL] [bit] NULL,
	[HOSPDAYS] [decimal](10, 2) NULL,
	[X_STAY] [bit] NULL,
	[DISABLE] [bit] NULL,
	[RECOVD] [nvarchar](max) NULL,
	[VAX_DATE] [datetime] NULL,
	[ONSET_DATE] [datetime] NULL,
	[NUMDAYS] [decimal](10, 2) NULL,
	[LAB_DATA] [nvarchar](max) NULL,
	[V_ADMINBY] [nvarchar](3) NULL,
	[V_FUNDBY] [nvarchar](max) NULL,
	[OTHER_MEDS] [nvarchar](max) NULL,
	[CUR_ILL] [nvarchar](max) NULL,
	[HISTORY] [nvarchar](max) NULL,
	[PRIOR_VAX] [nvarchar](max) NULL,
	[SPLTTYPE] [nvarchar](max) NULL,
	[FORM_VERS] [smallint] NULL,
	[TODAYS_DATE] [datetime] NULL,
	[BIRTH_DEFECT] [bit] NULL,
	[OFC_VISIT] [bit] NULL,
	[ER_ED_VISIT] [bit] NULL,
	[ALLERGIES] [nvarchar](max) NULL,
PRIMARY KEY CLUSTERED 
(
	[VAERS_ID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]
;

CREATE TABLE [VAX](
	[VAERS_ID] [int] NOT NULL,
	[VAX_TYPE] [nvarchar](max) NULL,
	[VAX_MANU] [nvarchar](max) NULL,
	[VAX_LOT] [nvarchar](max) NULL,
	[VAX_DOSE_SERIES] [nvarchar](max) NULL,
	[VAX_ROUTE] [nvarchar](max) NULL,
	[VAX_SITE] [nvarchar](max) NULL,
	[VAX_NAME] [nvarchar](max) NULL
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]
;

CREATE TABLE [sympt](
	[VAERS_ID] [int] NOT NULL,
	[SYMPTOM1] [nvarchar](max) NULL,
	[SYMPTOMVERSION1] [decimal](3, 1) NULL,
	[SYMPTOM2] [nvarchar](max) NULL,
	[SYMPTOMVERSION2] [decimal](3, 1) NULL,
	[SYMPTOM3] [nvarchar](max) NULL,
	[SYMPTOMVERSION3] [decimal](3, 1) NULL,
	[SYMPTOM4] [nvarchar](max) NULL,
	[SYMPTOMVERSION4] [decimal](3, 1) NULL,
	[SYMPTOM5] [nvarchar](max) NULL,
	[SYMPTOMVERSION5] [decimal](3, 1) NULL
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]
;

CREATE TABLE [range](
	[Date_Range] [nvarchar](50) NULL,
	[start_date] [datetime] NULL,
	[end_date] [datetime] NULL,
) ON [PRIMARY]
;

CREATE TABLE age_group (
    id INT PRIMARY KEY IDENTITY(1,1), -- Unique identifier for the age group
    name NVARCHAR(10) NOT NULL,       -- Descriptive label for the age group
    min_age INT NULL,                 -- Minimum age for the group (NULL for 'Unknown')
    max_age INT NULL,                 -- Maximum age for the group (NULL for 'Unknown')
    description NVARCHAR(255) NULL    -- Optional description of the group
);









