///////////////////////////////////////////////////////////////////////////
// C++ code generated with wxFormBuilder (version Oct 26 2018)
// http://www.wxformbuilder.org/
//
// PLEASE DO *NOT* EDIT THIS FILE!
///////////////////////////////////////////////////////////////////////////

#pragma once

#include <wx/artprov.h>
#include <wx/xrc/xmlres.h>
#include <wx/bitmap.h>
#include <wx/image.h>
#include <wx/icon.h>
#include <wx/statbmp.h>
#include <wx/gdicmn.h>
#include <wx/font.h>
#include <wx/colour.h>
#include <wx/settings.h>
#include <wx/string.h>
#include <wx/sizer.h>
#include <wx/panel.h>
#include <wx/textctrl.h>
#include <wx/splitter.h>
#include <wx/slider.h>
#include <wx/gauge.h>
#include <wx/notebook.h>
#include <wx/frame.h>

///////////////////////////////////////////////////////////////////////////


///////////////////////////////////////////////////////////////////////////////
/// Class MyFrame1
///////////////////////////////////////////////////////////////////////////////
class MyFrame1 : public wxFrame
{
	private:

	protected:
		wxNotebook* m_notebook1;
		wxPanel* m_panel4;
		wxSplitterWindow* m_splitter1;
		wxPanel* m_panel6;
		wxStaticBitmap* m_bitmap2;
		wxPanel* m_panel7;
		wxTextCtrl* m_textCtrl1;
		wxSplitterWindow* m_splitter2;
		wxPanel* m_panel8;
		wxSlider* m_slider2;
		wxGauge* m_gauge1;
		wxPanel* m_panel41;
		wxSplitterWindow* m_splitter11;
		wxPanel* m_panel61;
		wxStaticBitmap* m_bitmap21;
		wxPanel* m_panel71;
		wxTextCtrl* m_textCtrl11;
		wxSplitterWindow* m_splitter21;
		wxPanel* m_panel81;

	public:

		MyFrame1( wxWindow* parent, wxWindowID id = wxID_ANY, const wxString& title = wxEmptyString, const wxPoint& pos = wxDefaultPosition, const wxSize& size = wxSize( 600,500 ), long style = wxDEFAULT_FRAME_STYLE|wxTAB_TRAVERSAL );

		~MyFrame1();

		void m_splitter1OnIdle( wxIdleEvent& )
		{
			m_splitter1->SetSashPosition( 0 );
			m_splitter1->Disconnect( wxEVT_IDLE, wxIdleEventHandler( MyFrame1::m_splitter1OnIdle ), NULL, this );
		}

		void m_splitter2OnIdle( wxIdleEvent& )
		{
			m_splitter2->SetSashPosition( 0 );
			m_splitter2->Disconnect( wxEVT_IDLE, wxIdleEventHandler( MyFrame1::m_splitter2OnIdle ), NULL, this );
		}

		void m_splitter11OnIdle( wxIdleEvent& )
		{
			m_splitter11->SetSashPosition( 0 );
			m_splitter11->Disconnect( wxEVT_IDLE, wxIdleEventHandler( MyFrame1::m_splitter11OnIdle ), NULL, this );
		}

		void m_splitter21OnIdle( wxIdleEvent& )
		{
			m_splitter21->SetSashPosition( 0 );
			m_splitter21->Disconnect( wxEVT_IDLE, wxIdleEventHandler( MyFrame1::m_splitter21OnIdle ), NULL, this );
		}

};

