///////////////////////////////////////////////////////////////////////////
// C++ code generated with wxFormBuilder (version Oct 26 2018)
// http://www.wxformbuilder.org/
//
// PLEASE DO *NOT* EDIT THIS FILE!
///////////////////////////////////////////////////////////////////////////

#include "noname.h"

///////////////////////////////////////////////////////////////////////////

MyFrame1::MyFrame1( wxWindow* parent, wxWindowID id, const wxString& title, const wxPoint& pos, const wxSize& size, long style ) : wxFrame( parent, id, title, pos, size, style )
{
	this->SetSizeHints( wxDefaultSize, wxDefaultSize );

	wxBoxSizer* bSizer1;
	bSizer1 = new wxBoxSizer( wxVERTICAL );

	m_notebook1 = new wxNotebook( this, wxID_ANY, wxDefaultPosition, wxDefaultSize, 0 );
	m_panel4 = new wxPanel( m_notebook1, wxID_ANY, wxDefaultPosition, wxDefaultSize, wxTAB_TRAVERSAL );
	wxBoxSizer* bSizer3;
	bSizer3 = new wxBoxSizer( wxVERTICAL );

	m_splitter1 = new wxSplitterWindow( m_panel4, wxID_ANY, wxDefaultPosition, wxDefaultSize, wxSP_3D );
	m_splitter1->Connect( wxEVT_IDLE, wxIdleEventHandler( MyFrame1::m_splitter1OnIdle ), NULL, this );

	m_panel6 = new wxPanel( m_splitter1, wxID_ANY, wxDefaultPosition, wxSize( 295,295 ), wxTAB_TRAVERSAL );
	wxBoxSizer* bSizer6;
	bSizer6 = new wxBoxSizer( wxVERTICAL );

	bSizer6->SetMinSize( wxSize( 295,295 ) );
	m_bitmap2 = new wxStaticBitmap( m_panel6, wxID_ANY, wxBitmap( wxT("Cats/new_cats/av_cat/new_cat_av 07-09-2020 18:49.png"), wxBITMAP_TYPE_ANY ), wxDefaultPosition, wxDefaultSize, 0 );
	bSizer6->Add( m_bitmap2, 0, wxALL, 5 );


	m_panel6->SetSizer( bSizer6 );
	m_panel6->Layout();
	m_panel7 = new wxPanel( m_splitter1, wxID_ANY, wxDefaultPosition, wxSize( 295,295 ), wxTAB_TRAVERSAL );
	wxBoxSizer* bSizer7;
	bSizer7 = new wxBoxSizer( wxVERTICAL );

	bSizer7->SetMinSize( wxSize( 295,295 ) );
	m_textCtrl1 = new wxTextCtrl( m_panel7, wxID_ANY, wxEmptyString, wxDefaultPosition, wxDefaultSize, 0 );
	m_textCtrl1->SetForegroundColour( wxSystemSettings::GetColour( wxSYS_COLOUR_BACKGROUND ) );
	m_textCtrl1->SetBackgroundColour( wxSystemSettings::GetColour( wxSYS_COLOUR_3DDKSHADOW ) );
	m_textCtrl1->SetMinSize( wxSize( 295,295 ) );

	bSizer7->Add( m_textCtrl1, 0, wxALL, 5 );


	m_panel7->SetSizer( bSizer7 );
	m_panel7->Layout();
	m_splitter1->SplitVertically( m_panel6, m_panel7, 0 );
	bSizer3->Add( m_splitter1, 1, wxEXPAND, 5 );

	m_splitter2 = new wxSplitterWindow( m_panel4, wxID_ANY, wxDefaultPosition, wxDefaultSize, wxSP_3D );
	m_splitter2->Connect( wxEVT_IDLE, wxIdleEventHandler( MyFrame1::m_splitter2OnIdle ), NULL, this );

	m_panel8 = new wxPanel( m_splitter2, wxID_ANY, wxDefaultPosition, wxDefaultSize, wxTAB_TRAVERSAL );
	m_splitter2->Initialize( m_panel8 );
	bSizer3->Add( m_splitter2, 1, wxEXPAND, 5 );

	m_slider2 = new wxSlider( m_panel4, wxID_ANY, 1, 1, 200, wxPoint( -1,-1 ), wxSize( 295,10 ), wxSL_HORIZONTAL );
	bSizer3->Add( m_slider2, 0, wxALL, 5 );

	m_gauge1 = new wxGauge( m_panel4, wxID_ANY, 100, wxDefaultPosition, wxSize( 295,10 ), wxGA_HORIZONTAL );
	m_gauge1->SetValue( 0 );
	bSizer3->Add( m_gauge1, 0, wxALL, 5 );


	m_panel4->SetSizer( bSizer3 );
	m_panel4->Layout();
	bSizer3->Fit( m_panel4 );
	m_notebook1->AddPage( m_panel4, wxT("Spider"), true );
	m_panel41 = new wxPanel( m_notebook1, wxID_ANY, wxDefaultPosition, wxDefaultSize, wxTAB_TRAVERSAL );
	wxBoxSizer* bSizer31;
	bSizer31 = new wxBoxSizer( wxVERTICAL );

	m_splitter11 = new wxSplitterWindow( m_panel41, wxID_ANY, wxDefaultPosition, wxDefaultSize, wxSP_3D );
	m_splitter11->Connect( wxEVT_IDLE, wxIdleEventHandler( MyFrame1::m_splitter11OnIdle ), NULL, this );

	m_panel61 = new wxPanel( m_splitter11, wxID_ANY, wxDefaultPosition, wxSize( 295,295 ), wxTAB_TRAVERSAL );
	wxBoxSizer* bSizer61;
	bSizer61 = new wxBoxSizer( wxVERTICAL );

	bSizer61->SetMinSize( wxSize( 295,295 ) );
	m_bitmap21 = new wxStaticBitmap( m_panel61, wxID_ANY, wxBitmap( wxT("Cats/new_cats/av_cat/new_cat_av 07-09-2020 18:49.png"), wxBITMAP_TYPE_ANY ), wxDefaultPosition, wxDefaultSize, 0 );
	bSizer61->Add( m_bitmap21, 0, wxALL, 5 );


	m_panel61->SetSizer( bSizer61 );
	m_panel61->Layout();
	m_panel71 = new wxPanel( m_splitter11, wxID_ANY, wxDefaultPosition, wxSize( 295,295 ), wxTAB_TRAVERSAL );
	wxBoxSizer* bSizer71;
	bSizer71 = new wxBoxSizer( wxVERTICAL );

	bSizer71->SetMinSize( wxSize( 295,295 ) );
	m_textCtrl11 = new wxTextCtrl( m_panel71, wxID_ANY, wxEmptyString, wxDefaultPosition, wxDefaultSize, 0 );
	m_textCtrl11->SetForegroundColour( wxSystemSettings::GetColour( wxSYS_COLOUR_BACKGROUND ) );
	m_textCtrl11->SetBackgroundColour( wxSystemSettings::GetColour( wxSYS_COLOUR_3DDKSHADOW ) );
	m_textCtrl11->SetMinSize( wxSize( 295,295 ) );

	bSizer71->Add( m_textCtrl11, 0, wxALL, 5 );


	m_panel71->SetSizer( bSizer71 );
	m_panel71->Layout();
	m_splitter11->SplitVertically( m_panel61, m_panel71, 0 );
	bSizer31->Add( m_splitter11, 1, wxEXPAND, 5 );

	m_splitter21 = new wxSplitterWindow( m_panel41, wxID_ANY, wxDefaultPosition, wxDefaultSize, wxSP_3D );
	m_splitter21->Connect( wxEVT_IDLE, wxIdleEventHandler( MyFrame1::m_splitter21OnIdle ), NULL, this );

	m_panel81 = new wxPanel( m_splitter21, wxID_ANY, wxDefaultPosition, wxDefaultSize, wxTAB_TRAVERSAL );
	m_splitter21->Initialize( m_panel81 );
	bSizer31->Add( m_splitter21, 1, wxEXPAND, 5 );


	m_panel41->SetSizer( bSizer31 );
	m_panel41->Layout();
	bSizer31->Fit( m_panel41 );
	m_notebook1->AddPage( m_panel41, wxT("Explorer"), false );

	bSizer1->Add( m_notebook1, 1, wxEXPAND | wxALL, 5 );


	this->SetSizer( bSizer1 );
	this->Layout();

	this->Centre( wxBOTH );
}

MyFrame1::~MyFrame1()
{
}
